def find_unique_lines(file1, file2):
    try:
        # Read lines from file1 and create a set of lines
        with open(file1, 'r') as f1:
            lines_in_file1 = set(line.strip() for line in f1)

        # Read lines from file2 and check against the set from file1
        with open(file2, 'r') as f2:
            for line in f2:
                stripped_line = line.strip()
                if stripped_line not in lines_in_file1:
                    print(stripped_line)

    except FileNotFoundError:
        print(f"Error: One of the files ('{file1}' or '{file2}') not found.")

def main():
    file1 = 'file1.txt'  # Replace with the actual path to file1
    file2 = 'file2.txt'  # Replace with the actual path to file2

    find_unique_lines(file1, file2)

if __name__ == "__main__":
    main()
