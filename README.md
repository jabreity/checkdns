### DNS Zone File Processor

This Python script processes DNS Top-Level Domain (TLD) zone files (.txt and .txt.gz) and provides various forms of output based on command-line options. It supports reading files individually from a specified path or all files in a directory, ensuring efficient memory usage by processing files line by line.

#### Features

- **List Record Types**: Displays all unique record types present in the zone file(s).
- **List Records by Type**: Lists all records of a specified type (e.g., A, NS, AAAA, etc.).
- **List IP Addresses**: Retrieves all IP addresses present in A or AAAA records.
- **List Name Servers**: Outputs all name servers present in NS records.
- **List Records by Name Server**: Lists all records served by a specific name server.
- **List Records by Type by IP**: Displays all records of a specific type served by a specific IP address.
- **Compare Zone Files**: Optionally compares two sets of zone files and lists added/removed domains.
- **Multiple Output Formats**: Supports output to standard output (stdio), JSON files, or plain text files (.txt) based on user preference.
- **Input Sanitization**: Ensures safe file and directory input handling to prevent directory traversal.

#### Usage

1. **Installation**

   - Clone the repository:

     ```
     git clone https://github.com/jabreity/checkdns.git
     ```

   - Navigate to the directory:

     ```
     cd checkdns
     ```

2. **Running the Script**

   The script accepts the following command-line arguments:

   ```
   python checkdns.py <path_old> <path_new> [options]
   ```
   
- `<path_old>`: Path to old DNS TLD zone file or directory.
- `<path_new>`: Path to new DNS TLD zone file or directory.

- **Options**:

  - `--compare`: Compares old and new zone files and lists added/removed domains.
  - `--list-record-types`: Lists all record types present in the new zone file(s).
  - `--list-records-by-type <RECORD_TYPE>`: Lists all records of a specific type in the new zone file(s).
  - `--list-ip-addresses`: Lists all IP addresses present in A or AAAA records in the new zone file(s).
  - `--list-name-servers`: Lists all name servers present in NS records in the new zone file(s).
  - `--list-records-by-nameserver <NAMESERVER>`: Lists all records served by a specific name server in the new zone file(s).
  - `--list-records-by-type-by-ip <RECORD_TYPE> <IP_ADDRESS>`: Lists all records of a specific type served by a specific IP address in the new zone file(s).
  - `--output-types <OUTPUT_TYPES>`: Specifies output types (`stdio`, `json`, `txt`). Multiple types can be specified.

3. **Examples**

- Compare old and new zone files and list added/removed domains:

  ```
  python checkdns.py path_old/zonefile.txt path_new/zonefile.txt --compare
  ```

- List all record types present in the new zone files:

  ```
  python checkdns.py path_old/zonefile.txt path_new/zonefile.txt --list-record-types
  ```

- List all A records in the new zone files:

  ```
  python checkdns.py path_old/zonefile.txt path_new/zonefile.txt --list-records-by-type A
  ```

- Output results in JSON format:

  ```
  python checkdns.py path_old/zonefile.txt path_new/zonefile.txt --list-record-types --output-types json
  ```

4. **Output**

- By default, results are printed to standard output (`stdio`).
- Specify `--output-types json` or `--output-types txt` to save results to JSON or plain text files, respectively.

#### Notes

- Ensure Python 3.x is installed on your system.
- The script does not load entire files into memory at once, ensuring efficient processing of large zone files.

#### License

This project is licensed under the MIT License - see the LICENSE file for details.

#### Authors

-Jason (jabreity) Breitwieser

#### Acknowledgments

- Inspired by [OpenAI](https://www.openai.com)'s GPT-3 model.

Feel free to customize this `README.md` according to your project specifics, including adding contact information, acknowledgments, and any additional instructions or features relevant to your use case.
