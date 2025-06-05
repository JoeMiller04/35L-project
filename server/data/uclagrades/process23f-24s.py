"""
This is a script to process the UCLA grades data for the 2023 Summer through 2024 Spring semesters.
It includes functions to read the data, clean it, and save it to a MongoDB database.
Run from inside the data/uclagrades directory.
IF YOU RUN MULTIPLE TIMES, IT WILL CONTINUE TO APPEND TO THE DATABASE.
"""

import pandas as pd
import sys
import os
import argparse

def process_grades_file(file="grades-23f-24s.csv"):
    

    column_names = ['term', 'long subject', 'catalog', 'section', 'grade',
        'grade_count', 'enrolled_total', 'instructor', 'unused_INSTR_CD', 'title',
        'subject', 'unused_INTL_CATL', 'unused_INTL_SECT'] # column names for importing

    df = pd.read_csv(file, header=None, names=column_names)
    use_columns = ['term', 'subject', 'catalog', 'section', 'grade',
        'grade_count', 'enrolled_total', 'instructor', 'title']
    df = df[use_columns] # select the columns we wil actually use

    # Sanity Checks
    assert int(df.isna().sum().sum()) == 0 # We shouldn't have missing data for this file
    assert len(df) == 47743 # There should be 47743 points for 23F-24S

    df = df.drop(index=0) # drop the first row because it's just headers

    # Convert some columns to numeric
    df["grade_count"] = pd.to_numeric(df["grade_count"])
    df["enrolled_total"] = pd.to_numeric(df["enrolled_total"])

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
    pivot["P"] = pivot["P"] + pivot["S"]
    pivot["NP"] = pivot["NP"] + pivot["U"]
    pivot["F"] = pivot["F"] + pivot["NC"]
    pivot.drop(columns=["S", "U", "NC"], inplace=True)
    extra = ["DR", "I"]
    pivot["other"] = pivot[extra].sum(axis=1)
    pivot.drop(columns=extra, inplace=True)

    pivot["real"] = True # So we know this is real data

    # In 22F-23S, we only had 17 rows that didn't match up for enrollment totals
    # But for here, we have 1,000+ rows that don't match up.
    # So let's just keep them even if they don't match up.
    filtered = (
        pivot
        .loc[pivot["real"]]   # keep only the good rows
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
    from pymongo import MongoClient
    import os
    
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "35L-project")
    
    try:
        # Connect to MongoDB
        print(f"Connecting to MongoDB at {MONGO_URI}...")
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
        # collection.drop()
        
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
    from pymongo import MongoClient
    import os
    
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "35L-project")
    
    try:
        # Connect to MongoDB
        print(f"Connecting to MongoDB at {MONGO_URI}...")
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


def main():
    parser = argparse.ArgumentParser(description="Process UCLA grades data and save to MongoDB")
    parser.add_argument("file_path", nargs="?", default="grades-23f-24s.csv", 
                        help="Path to the grades CSV file (default: grades-23f-24s.csv)")
    args = parser.parse_args()
    print("Processing UCLA grades data from 2023 Summer to 2024 Spring...")
    tidy = process_grades_file(args.file_path)
    print("Exporting data to MongoDB...")
    count = export_to_mongodb(tidy)
    fix_trailing_spaces()
    print(f"Export completed. {count} records exported.")


# Call the export function
if __name__ == "__main__":
    main()

