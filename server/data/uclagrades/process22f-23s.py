"""
This is a script to process the UCLA grades data for the 2022 Fall and 2023 Spring semesters.
It includes functions to read the data, clean it, and save it to a MongoDB database.
Run from inside the data/uclagrades directory.
IF YOU RUN MULTIPLE TIMES, IT WILL CONTINUE TO APPEND TO THE DATABASE.
"""

import pandas as pd

file  = "grades-22f-23s.csv"

column_names = ['term', 'subject', 'catalog', 'section', 'grade',
       'grade_count', 'enrolled_total', 'instructor', 'unused_INSTR_CD', 'title',
       'unused_ENROL_TERM_SEQ_NBR', 'unused_INTL_CATL', 'unused_INTL_SECT', 'unused_CREATION_DATE',
       'unused_ROWNO'] # column names for importing the data

df = pd.read_csv(file, header=None, names=column_names)
use_columns = ['term', 'subject', 'catalog', 'section', 'grade',
       'grade_count', 'enrolled_total', 'instructor', 'title']
df = df[use_columns] # select the columns we wil actually use

# Sanity Checks
assert int(df.isna().sum().sum()) == 0 # We shouldn't have missing data for this file
assert len(df) == 37002 # There should be 37002 points


# grp_cols = ["term", "subject", "catalog", "instructor", "title"]
grp_cols = ["term", "subject", "catalog", "instructor", "title", "section"]
"""
The same instance of class should have all these columns be the same
I thought using the "section" column would be redundant, 
but it's not and it changes the number of groups we have (by like 1000)
TODO check what the differences are 
I've noticed that there's only 17 mismatched columns for enrollment totals
when I use section, otherwise there's 500~600 where it doesn't add up right
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
pivot["P"] = pivot["P"] + pivot["S"]
pivot["NP"] = pivot["NP"] + pivot["U"]
pivot.drop(columns=["S", "U"], inplace=True)
extra = ["DR", "I", "IP", "LI", "NR", "R"]
pivot["other"] = pivot[extra].sum(axis=1)
pivot.drop(columns=extra, inplace=True)

pivot["real"] = True # So we know this is real data

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
# tidy.to_csv("grades_backup_23f-23s.csv", index=False)

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
        
        # Uncomment the next line to drop the collection if needed
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
    

def fix_catalog_spaces():
    """Fix trailing spaces in catalog numbers in existing MongoDB collection"""
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
            if 'catalog' in course and isinstance(course['catalog'], str):
                stripped = course['catalog'].strip()
                if stripped != course['catalog']:
                    collection.update_one(
                        {"_id": course["_id"]},
                        {"$set": {"catalog": stripped}}
                    )
                    fixed_count += 1
        
        print(f"Fixed trailing spaces in {fixed_count} records")
        return fixed_count
    
    except Exception as e:
        print(f"Error fixing catalog spaces: {e}")
        return 0


# Call the export function
if __name__ == "__main__":
    print("Exporting data to MongoDB...")
    count = export_to_mongodb(tidy)
    fix_catalog_spaces()
    print(f"Export completed. {count} records exported.")
