"""
This is a script to process the UCLA grades data for the 2021 Fall through 2022 Summer semesters.
It includes functions to read the data, clean it, and save it to a MongoDB database.
Run from inside the data/uclagrades directory.
IF YOU RUN MULTIPLE TIMES, IT WILL CONTINUE TO APPEND TO THE DATABASE.
"""

import pandas as pd
import sys
import os
import argparse
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


def process_grades_file(file_path):
    """Process the grades file and return a cleaned DataFrame"""
    print(f"Processing grades data from {file_path}...")
    
    column_names = ['term', 'subject', 'catalog', 'section', 'grade',
           'grade_count', 'enrolled_total', 'instructor', 'unused_INSTR_CD', 'title',
           'idk', 'unused_INTL_CATL', 'unused_INTL_SECT', "creation_date", "idk2"] # column names for importing

    df = pd.read_csv(file_path, header=None, names=column_names)
    use_columns = ['term', 'subject', 'catalog', 'section', 'grade',
           'grade_count', 'enrolled_total', 'instructor', 'title']
    df = df[use_columns] # select the columns we wil actually use

    # Sanity Checks
    assert int(df.isna().sum().sum()) == 0 # We shouldn't have missing data for this file


    # grp_cols = ["term", "subject", "catalog", "instructor", "title"]
    grp_cols = ["term", "subject", "catalog", "instructor", "title", "section"]
    """
    Enrollment totals do not always match up to the sum of the grades.
    We could investigate this, but I don't think it's worth it for now.
    """

    # So we group by them by same instance of course
    # And collapse grades
    g_counts = (df.groupby(grp_cols + ["grade"], as_index=False).agg(total=("grade_count", "sum")))

    # Make grades into their own columns
    pivot = (g_counts.pivot_table(index=grp_cols, columns="grade", values="total", fill_value=0).reset_index())

    grade_cols = df["grade"].unique() # every grade column in the DataFrame
    pivot["enrolled_total_calc"] = pivot[grade_cols].sum(axis=1)

    # bring back the original ENRL TOT to compare
    enrl_tot = (df.drop_duplicates(subset=grp_cols)
                  [grp_cols + ["enrolled_total"]])

    pivot = pivot.merge(enrl_tot, on=grp_cols, how="left")

    pivot["enrl_mismatch"] = pivot["enrolled_total_calc"] != pivot["enrolled_total"]

    print("Grouped into", len(pivot), "distinct courses")
    bad = pivot[pivot["enrl_mismatch"]]
    print("There are", len(bad), "courses where total grades don't match up to enrolled total")

    # For the MongoDB we will keep the computed total
    pivot.drop(columns=["enrolled_total"], inplace=True)
    pivot.rename(columns={"enrolled_total_calc": "enrolled_total"}, inplace=True)


    # For some reason every grade is three characters. So "A" is really "A  " with 
    # two trailing spaces. Let's get rid of those.
    gradeMap = {}
    for grade in grade_cols:
      gradeMap[grade] = grade.rstrip()
    pivot.rename(columns=gradeMap, inplace=True)


    # I don't think we really need all the 'extra' grades.
    # I belive S/U are equivalent to P/NP but just for grad class, 
    # and the other grades can fall under "Other"
    # Then all the grades we have are A~F, P/NP, and other
    # Also for this dataset, NC (no credit) is combined with F
    pivot["P"] = pivot.get("P", 0) + pivot.get("S", 0)
    pivot["NP"] = pivot.get("NP", 0) + pivot.get("U", 0)
    pivot["F"] = pivot.get("F", 0) + pivot.get("NC", 0)
    
    # Drop columns if they exist
    for col in ["S", "U", "NC"]:
        if col in pivot.columns:
            pivot.drop(columns=[col], inplace=True)
    
    extra = ["DR", "I", "IP", "R", "NR"]
    # Only sum columns that exist
    extra_cols = [col for col in extra if col in pivot.columns]
    pivot["other"] = pivot[extra_cols].sum(axis=1) if extra_cols else 0
    
    # Drop columns if they exist
    for col in extra:
        if col in pivot.columns:
            pivot.drop(columns=[col], inplace=True)

    pivot["real"] = True # So we know this is real data

    # Only 22 coures have mismatched enrollments for this dataset
    # So let's drop those
    filtered = (
        pivot
        .loc[~pivot["enrl_mismatch"] & pivot["real"]]   # keep only the good rows
        .drop(columns=["enrl_mismatch"])                # drop this column
        .reset_index(drop=True)
    )

    remaining_grades = ['A+', "A", 'A-', 'B', 'B+', 'B-', 'C', 'C+', 'C-', 'D', 'D+', 'D-', 'F','NP', 'P', "other"]
    filtered["grades"] = (
        pivot[remaining_grades]
        .astype("int")               
        .apply(lambda r: r.to_dict(), axis=1)
    )
    tidy = filtered.drop(columns=remaining_grades)

    print("Exporting", len(tidy), "rows")
    return tidy

def export_to_mongodb(data):
    """Export the processed data to MongoDB"""
    
    try:
        # Connect to MongoDB
        print(f"Connecting to MongoDB at {MONGO_URI}...")
        if not MONGO_URI or not DATABASE_NAME:
            print("MONGO_URI or DATABASE_NAME is not set in the environment variables.")
            return
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        
        # Add a timestamp for the import
        import datetime
        import_time = datetime.datetime.now()
        
        # Convert DataFrame to list of dictionaries for MongoDB insertion
        records = data.to_dict('records')
        for record in records:
            record['import_date'] = import_time
            
        # Insert into valid_courses collection
        collection = db["courses"]
        
        # Uncomment the next line to clear the collection if needed
        collection.drop()
        
        collection.create_index([
            ("term", 1),
            ("subject", 1),
            ("catalog", 1),
            ("instructor", 1)
        ])
        
        # Insert the records
        result = collection.insert_many(records)
        
        print(f"Successfully inserted {len(result.inserted_ids)} documents into MongoDB")
        return len(result.inserted_ids)
    
    except Exception as e:
        print(f"Error exporting to MongoDB: {e}")
        return 0
    

def fix_trailing_spaces():
    """Fix trailing spaces in several fields in existing MongoDB collection
    For some reason, the original data has trailing spaces in several columns.
    Currently fixes the catalog, subject, and section fields."""
    
    try:
        # Connect to MongoDB
        print(f"Connecting to MongoDB at {MONGO_URI}...")
        if not MONGO_URI or not DATABASE_NAME:
            print("MONGO_URI or DATABASE_NAME is not set in the environment variables.")
            return
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db["courses"]
        
        # Get all courses
        courses = list(collection.find({}))
        fixed_count = 0
        
        # Fix each course
        for course in courses:
            updates = {}
            
            # Check catalog field
            if 'catalog' in course and isinstance(course['catalog'], str):
                stripped = course['catalog'].strip()
                if stripped != course['catalog']:
                    updates['catalog'] = stripped
            
            # Check subject field
            if 'subject' in course and isinstance(course['subject'], str):
                stripped = course['subject'].strip()
                if stripped != course['subject']:
                    updates['subject'] = stripped
            
            # Check section field
            if 'section' in course and isinstance(course['section'], str):
                stripped = course['section'].strip()
                if stripped != course['section']:
                    updates['section'] = stripped
            
            # Update the document if any fields need fixing
            if updates:
                collection.update_one(
                    {"_id": course["_id"]},
                    {"$set": updates}
                )
                fixed_count += 1
        
        print(f"Fixed trailing spaces in {fixed_count} records")
        return fixed_count
    
    except Exception as e:
        print(f"Error fixing spaces: {e}")
        return 0


# Main function that handles command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Process UCLA grades data and save to MongoDB")
    parser.add_argument("file_path", nargs="?", default="grades-21f-222.csv", 
                        help="Path to the grades CSV file (default: grades-21f-222.csv)")
    parser.add_argument("--skip-upload", action="store_true", 
                        help="Skip uploading to MongoDB (only process data)")
    parser.add_argument("--output", "-o", type=str, 
                        help="Save processed data to this CSV file")
    
    args = parser.parse_args()
    
    # Check if the file exists
    if not os.path.exists(args.file_path):
        print(f"Error: File not found: {args.file_path}")
        return 1
    
    try:
        # Process the file
        processed_data = process_grades_file(args.file_path)
        
        # Save to CSV if requested
        if args.output:
            processed_data.to_csv(args.output, index=False)
            print(f"Saved processed data to {args.output}")
        
        # Upload to MongoDB unless skipped
        if not args.skip_upload:
            print("Exporting data to MongoDB...")
            count = export_to_mongodb(processed_data)
            fix_trailing_spaces()
            print(f"Export completed. {count} records exported.")
        
        return 0
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return 1


# Call the main function
if __name__ == "__main__":
    sys.exit(main())
