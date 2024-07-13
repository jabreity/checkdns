```markdown
# checkdns.py

## Description
`checkdns.py` is a Python script designed to process DNS TLD zone files and provide various forms of output based on command-line options. It supports operations such as listing IP addresses, nameservers, specific record types, and more, with options to output results in JSON, TXT formats, or to standard output.

## Features
- Process DNS TLD zone files (.txt and .txt.gz formats).
- Supports input from files or directories.
- Memory-efficient processing for handling large zone files.
- Various operations supported including listing IPs, nameservers, record types, etc.
- Flexible output options (JSON, TXT).

## Usage
```bash
python checkdns.py [options] inputs...
```

## Options
- `--list-ip`: List all IP addresses within the input.
- `--list-nameservers`: List all nameservers within the input.
- `--list-records-by-nameserver NAMESERVER`: List all records with a specific nameserver within input.
- `--list-record-types`: List all record types within input.
- `--output-json`: Output results in JSON format.
- `--output-txt`: Output results in TXT format.
- `--output-by-type-by-ip`: Output records by type by IP.
- `--list-nameservers-by-type RECORD_TYPE`: List all nameservers with a specific record type.
- `--list-record-types-by-nameserver NAMESERVER`: List all record types by nameserver.
- `--list-records-by-ttl TTL`: List all records by TTL.
- `--list-all-ttl-values`: List all TTL values.
- `--list-dnssec-public-keys`: List all DNSSEC public keys.
- `--validate-dnssec-public-keys`: Validate all DNSSEC public keys.

## Examples
```bash
# List all IP addresses in the provided directory
python checkdns.py --list-ip /path/to/directory

# List all nameservers and output in JSON format
python checkdns.py --list-nameservers --output-json /path/to/file.txt /path/to/another_directory

# Compare two directories of zone files
python checkdns.py --compare /path/to/directory1 /path/to/directory2
```

## Contributors
- Jason "jabreity" Breitwieser
- ChatGPT (OpenAI)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
```

This `README.md` file provides a concise overview of the `checkdns.py` script, including its description, features, usage examples, options available, contributors, and licensing information. Adjustments can be made based on specific details or additional functionalities of the script.
