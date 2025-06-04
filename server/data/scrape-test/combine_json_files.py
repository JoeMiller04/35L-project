import os
import json
import glob
import argparse

def combine_json_files(directory='.',output_file='combined_courses.json'):
    """
    Combine multiple JSON files into one super file
    
    Parameters:
    - directory: Directory containing the JSON files
    - output_file: Name of the output file
    
    Returns:
    - Count of files processed and total courses combined
    """

    pattern = "*.json"
    # Get a list of all JSON files matching the pattern
    file_paths = glob.glob(os.path.join(directory, pattern))
    print(f"Found {len(file_paths)} files matching pattern '{pattern}'")
    
    # Combined array to hold all courses
    all_courses = []
    
    
    # Process each file
    for file_path in sorted(file_paths):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Try to load the file as JSON
                data = json.load(f)
                
                # If it's a list, extend our array
                if isinstance(data, list):
                    # Track file statistics
                    courses_in_file = len(data)
                    courses_added = 0
                    
                    # Add each course if it's not a duplicate
                    for course in data:
                        # Check if course has required fields (subject, time, instructor, title, time)
                        if not isinstance(course, dict) or 'subject' not in course or 'time' not in course or 'instructor' not in course or 'title' not in course:
                            print(f"Skipping course with missing fields in {file_path}: {course}")
                            continue
                        
                        all_courses.append(course)
                        courses_added += 1
                    
                    print(f"Processed {file_path}: {courses_added} courses added (of {courses_in_file} in file)")
                else:
                    print(f"Skipping {file_path}: Not a JSON array")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Save the combined data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_courses, f, indent=2)
    
    print(f"\nCombination complete: {len(file_paths)} files processed")
    print(f"Total unique courses: {len(all_courses)}")
    print(f"Saved to: {output_file}")
    
    return len(file_paths), len(all_courses)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine multiple JSON course files into one")
    parser.add_argument("--dir", default=".", help="Directory containing JSON files")
    parser.add_argument("--output", default="combined_courses.json", help="Output file name")
    
    args = parser.parse_args()
    combine_json_files(args.dir, args.output)