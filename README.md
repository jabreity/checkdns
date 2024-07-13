# DNS Zone File Processor

## Description
This Python script `checkdns.py` processes DNS zone files to extract various information such as nameservers, IP addresses, and different types of DNS records. It supports both plain text (.txt) and gzip compressed (.txt.gz) files.

## Features
- **List Nameservers**: Extracts all nameservers from the input zone files.
- **List IP Addresses**: Extracts all IP addresses from the input zone files.
- **Filter Records by Nameserver**: Extracts records associated with a specific nameserver.
- **List Record Types**: Extracts all types of DNS records present in the input files.
- **Output Formats**: Supports output in JSON and plaintext formats.
  
## Usage
To use the script, execute it with Python, providing necessary arguments:

```bash
python checkdns.py <inputs> [--gzip] [--list-nameservers] [--list-ips] [--nameserver <nameserver>] [--list-record-types] [--output-format <format>] [--output-file <file>]
```

### Arguments:
- `<inputs>`: One or more input zone files or directories containing zone files.
- `--gzip`: Optional flag to constrain input to .txt.gz files.
- `--list-nameservers`: Optional flag to list all nameservers found.
- `--list-ips`: Optional flag to list all IP addresses found.
- `--nameserver <nameserver>`: Optional flag to filter records by a specific nameserver.
- `--list-record-types`: Optional flag to list all DNS record types found.
- `--output-format <format>`: Optional flag to specify output format (`json` or `txt`). Default is `json`.
- `--output-file <file>`: Optional flag to specify the output file path.

## Examples
### Example 1: List all nameservers in a directory of zone files
```bash
python checkdns.py /path/to/zone/files --list-nameservers
```

### Example 2: Filter records by a specific nameserver and save output to JSON file
```bash
python checkdns.py /path/to/zone/file.txt --nameserver ns1.example.com --output-format json --output-file output.json
```

## Requirements
- Python 3.x
- `argparse` module (typically included in Python standard library)

## Author
- Jason "jabreity" Breitwieser
- OpenAI ChatGPT (assistant for writing this README)

```

Feel free to customize the examples or add more details as per your specific use cases or preferences. Adjust the paths and examples to reflect how users are expected to interact with your script in their environment.
