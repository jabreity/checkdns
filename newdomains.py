import os
import argparse
import gzip

def is_gzip_file(filepath):
    """ Check if a file is a valid gzip file by attempting to read the gzip magic number. """
    try:
        with open(filepath, 'rb') as f:
            return f.read(2) == b'\x1f\x8b'  # Check for gzip magic number
    except IOError:
        return False

def find_unique_lines(dir1, dir2):
    # Get list of files in dir1 and dir2
    files_in_dir1 = os.listdir(dir1)
    files_in_dir2 = os.listdir(dir2)

    # Filter out non-gzip files from dir1
    files_in_dir1 = [f for f in files_in_dir1 if is_gzip_file(os.path.join(dir1, f))]

    # Read lines from files in dir1 and store in a dictionary of sets
    lines_in_dir1 = {}
    for file1 in files_in_dir1:
        lines_in_dir1[file1] = set()
        with gzip.open(os.path.join(dir1, file1), 'rt') as f1:
            for line in f1:
                lines_in_dir1[file1].add(line.strip())

    # Iterate through files in dir2
    for file2 in files_in_dir2:
        if not is_gzip_file(os.path.join(dir2, file2)):
            print(f"Skipping non-gzip file: {file2}")
            continue
        
        unique_lines = set()
        with gzip.open(os.path.join(dir2, file2), 'rt') as f2:
            for line in f2:
                stripped_line = line.strip()
                found_unique = True
                # Check against all sets from dir1
                for key, lines_set in lines_in_dir1.items():
                    if stripped_line in lines_set:
                        found_unique = False
                        break
                if found_unique:
                    unique_lines.add(stripped_line)

        # Print unique lines for each file in dir2
        print(f"Unique lines in {file2}:")
        for line in unique_lines:
            print(line)
        print()  # Print an empty line for separation

def main():
    parser = argparse.ArgumentParser(description='Compare gzipped domain files in two directories')
    parser.add_argument('dir1', help='Path to the first directory containing gzipped domain files')
    parser.add_argument('dir2', help='Path to the second directory containing gzipped domain files')
    args = parser.parse_args()

    find_unique_lines(args.dir1, args.dir2)

if __name__ == "__main__":
    main()
