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

def find_new_domains(file1, file2, field_num):
    # Extract unique field values from both files
    field_values1 = extract_unique_fields(file1, field_num)
    field_values2 = extract_unique_fields(file2, field_num)

    # Find new domains (field values) in file2 that are not in file1
    new_domains = field_values2 - field_values1

    # Print new domains
    print(f"\nNew domains found in {file2} but not in {file1}:")
    for domain in sorted(new_domains):
        print(f"  {domain}")

def main():
    parser = argparse.ArgumentParser(description='Compare gzipped zone files')
    parser.add_argument('file1', help='Path to the first gzipped file')
    parser.add_argument('file2', help='Path to the second gzipped file')
    parser.add_argument('-f', '--field', type=int, default=4, help='Field number to extract (default is 4)')
    args = parser.parse_args()

    file1 = args.file1
    file2 = args.file2
    field_num = args.field

    if os.path.isfile(file1) and os.path.isfile(file2):
        find_new_domains(file1, file2, field_num)
    else:
        print("Error: Please provide two valid gzipped files.")

if __name__ == "__main__":
    main()
