import argparse
import os
import gzip

def process_directories(dir1, dir2, field_num):
    files1 = find_gz_files(dir1)
    files2 = find_gz_files(dir2)

    for filename1 in files1:
        basename1 = os.path.basename(filename1)
        matching_file2 = os.path.join(dir2, basename1)
        if matching_file2 in files2:
            print(f"\nComparing files: {filename1} and {matching_file2}\n")
            compare_files(filename1, matching_file2, field_num)

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
        print(f"\nComparing files: {dir1} and {dir2}\n")
        compare_files(dir1, dir2, field_num)
    elif os.path.isdir(dir1) and os.path.isdir(dir2):
        # Compare files with matching names in two directories
        process_directories(dir1, dir2, field_num)
    else:
        print("Error: Please provide two files or two directories.")

if __name__ == "__main__":
    main()
