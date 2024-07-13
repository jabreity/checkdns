import argparse
import os
import gzip

def extract_fields(filename, field_num):
    fields_list = []

    try:
        with gzip.open(filename, 'rt') as file:
            for line in file:
                if line.startswith(';') or line.strip() == '':
                    continue

                fields = line.split()
                if len(fields) >= field_num:
                    fields_list.append(fields[field_num - 1])

        return fields_list

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

def count_record_types(filename):
    record_types = {
        'a': 0,
        'aaaa': 0,
        'dnskey': 0,
        'ds': 0,
        'ns': 0,
        'nsec3': 0,
        'nsec3param': 0,
        'rrsig': 0,
        'soa': 0
    }

    try:
        with gzip.open(filename, 'rt') as file:
            for line in file:
                if line.startswith(';') or line.strip() == '':
                    continue

                fields = line.split()
                if len(fields) >= 4 and fields[3] in record_types:
                    record_types[fields[3]] += 1

        return record_types

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}

def compare_files(file1, file2, field_num, output_field):
    # Extract fields from both files
    fields1 = extract_fields(file1, field_num)
    fields2 = extract_fields(file2, field_num)

    # Calculate differences
    added_values = list(set(fields2) - set(fields1))
    removed_values = list(set(fields1) - set(fields2))

    if output_field:
        added_values = [fields2[i] for i in range(len(fields2)) if fields2[i] in added_values]

    # Print results
    print(f"\nComparing files: {file1} and {file2}\n")
    print(f"Values added in {file2} but not in {file1}: {len(added_values)}")
    for value in added_values:
        print(f"  {value}")

    if output_field:
        print(f"Values removed in {file2} but not in {file1}: {len(removed_values)}")
        for value in removed_values:
            print(f"  {value}")

def process_directories(dir1, dir2, field_num, output_field):
    files1 = find_gz_files(dir1)
    files2 = find_gz_files(dir2)

    for filename in files1:
        basename = os.path.basename(filename)
        matching_file = os.path.join(dir2, basename)
        if matching_file in files2:
            compare_files(filename, matching_file, field_num, output_field)

def find_gz_files(directory):
    gz_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.gz'):
                gz_files.append(os.path.join(root, file))
    return gz_files

def main():
    parser = argparse.ArgumentParser(description='Compare gzipped zone files or directories')
    parser.add_argument('dir1', help='Path to the first directory or gzipped file')
    parser.add_argument('dir2', help='Path to the second directory or gzipped file')
    parser.add_argument('-f', '--field', type=int, help='Field number to extract (default is 4)', default=4)
    parser.add_argument('--output-field', action='store_true', help='Output the selected field only')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    dir1 = args.dir1
    dir2 = args.dir2
    field_num = args.field
    output_field = args.output_field
    debug_mode = args.debug

    if debug_mode:
        # Enable debug mode: Print all fields and record types
        print("Debug mode enabled.\n")
        print("All fields and record types in each file:\n")
        process_directories(dir1, dir2, field_num, output_field)
    else:
        # Compare files or directories based on arguments
        if os.path.isfile(dir1) and os.path.isfile(dir2):
            # Compare two individual files
            compare_files(dir1, dir2, field_num, output_field)
        elif os.path.isdir(dir1) and os.path.isdir(dir2):
            # Compare files with matching names in two directories
            process_directories(dir1, dir2, field_num, output_field)
        else:
            print("Error: Please provide two files or two directories.")

if __name__ == "__main__":
    main()
