import argparse
import re

def parse_zone_file(file_path):
    """Parses a zone file line by line, yielding record data.

    Args:
        file_path: Path to the zone file.

    Yields:
        A tuple containing the line number, line content, and a boolean indicating if the line is a comment.
    """
    with open(file_path, 'r') as f:
        line_number = 0
        for line in f:
            line_number += 1
            print(f"Processing line {line_number}")  # Add debugging print
            line = line.strip()
            if not line or line.startswith(';'):
                yield line_number, line, True
            else:
                yield line_number, line, False

# ... rest of the code

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
