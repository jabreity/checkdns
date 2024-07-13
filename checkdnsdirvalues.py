import argparse
import os
import gzip

def extract_unique_fields(filename, field_num):
    field_values = set()

    try:
        with gzip.open(filename, 'rt') as file:
            for line in file:
                if line.startswith(';') or line.strip() == '':
                    continue
                
                fields = line.split()
                if len(fields) >= field_num:
                    field_values.add(fields[field_num - 1])

        return field_values

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return set()

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

def compare_files(file1, file2, field_num):
    # Extract unique field values and record type counts for both files
    field_values1 = extract_unique_fields(file1, field_num)
    field_values2 = extract_unique_fields(file2, field_num)

    record_types1 = count_record_types(file1)
    record_types2 = count_record_types(file2)

    # Identify differences
    unique_in_file1 = field_values1 - field_values2
    unique_in_file2 = field_values2 - field_values1

    diff_record_types = {}
    for record_type in record_types1:
        if record_types1[record_type] != record_types2.get(record_type, 0):
            diff_record_types[record_type] = (record_types1[record_type], record_types2.get(record_type, 0))

    # Print results
    print(f"\nComparing files: {file1} and {file2}\n")

    print(f"Unique field values in {file1} but not in {file2}:")
    for value in sorted(unique_in_file1):
        print(f"  {value}")

    print(f"\nUnique field values in {file2} but not in {file1}:")
    for value in sorted(unique_in_file2):
        print(f"  {value}")

    print("\nDifferences in record type counts:")
    for record_type, counts in diff_record_types.items():
        print(f"  {record_type}: {file1}={counts[0]}, {file2}={counts[1]}")

    print(f"\nRecord type counts in {file1}:")
    for record_type, count in record_types1.items():
        print(f"  {record_type}: {count}")

    print(f"\nRecord type counts in {file2}:")
    for record_type, count in record_types2.items():
        print(f"  {record_type}: {count}")

def process_directories(dir1, dir2, field_num):
    files1 = find_gz_files(dir1)
    files2 = find_gz_files(dir2)

    for filename in files1:
        basename = os.path.basename(filename)
        matching_file = os.path.join(dir2, basename)
        if matching_file in files2:
            compare_files(filename, matching_file, field_num)

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
    parser.add_argument('-f', '--field', type=int, help='Field number to extract (default is 4)')
    args = parser.parse_args()

    dir1 = args.dir1
    dir2 = args.dir2
    field_num = args.field if args.field else 4

    if os.path.isfile(dir1) and os.path.isfile(dir2):
        # Compare two individual files
        compare_files(dir1, dir2, field_num)
    elif os.path.isdir(dir1) and os.path.isdir(dir2):
        # Compare files with matching names in two directories
        process_directories(dir1, dir2, field_num)
    else:
        print("Error: Please provide two files or two directories.")

if __name__ == "__main__":
    main()
