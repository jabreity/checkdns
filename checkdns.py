#!/bin/python3
import os
import sys
import gzip
import json
from dns import resolver, reversename
from optparse import OptionParser

def process_dns_zone_file(zone_file):
    with open(zone_file, 'r') as f:
        for line in f:
            if line.strip().endswith(';'):
                continue
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            name, type, value = parts[:3]
            try:
                ip = resolver.query(name + '.' + value, 'A').response.answer[0].items[0].rdata
            except:
                continue
            print(f"{name} {type} {value} {ip}")

def process_dns_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt.gz'):
                with gzip.open(os.path.join(root, file), 'rt') as f:
                    for line in f:
                        if line.strip().endswith(';'):
                            continue
                        parts = line.strip().split()
                        if len(parts) < 3:
                            continue
                        name, type, value = parts[:3]
                        try:
                            ip = resolver.query(name + '.' + value, 'A').response.answer[0].items[0].rdata
                        except:
                            continue
                        print(f"{name} {type} {value} {ip}")

def main():
    parser = OptionParser()
    parser.add_option('-c', '--compare', action='store_true', help='compare zone files or directories')
    parser.add_option('-d', '--directory', action='store', help='process a directory of zone files')
    parser.add_option('-f', '--file', action='store', help='process a single zone file')
    parser.add_option('--gzip', action='store_true', help='only process.txt.gz files in directory')
    parser.add_option('-o', '--output', choices=['json', 'txt', 'stdio'], help='output format')
    parser.add_option('-l', '--list-ip', action='store_true', help='list all IP addresses')
    parser.add_option('-n', '--list-nameserver', action='store_true', help='list all nameservers')
    parser.add_option('-r', '--record-type', action='store', help='list all records of specific type')
    parser.add_option('-t', '--ttl', action='store_true', help='list all TTL values')
    parser.add_option('-v', '--dnssec', action='store_true', help='validate DNSSEC public keys')

    options, args = parser.parse_args()

    if options.compare:
        if len(args)!= 2:
            parser.error('compare requires two inputs')
        file1, file2 = args
        process_dns_zone_file(file1)
        process_dns_zone_file(file2)
    elif options.directory:
        process_dns_directory(options.directory)
    elif options.file:
        process_dns_zone_file(options.file)

    if options.output == 'json':
        print(json.dumps([]))
    elif options.output == 'txt':
        print()

    if options.list_ip:
        print('IP Addresses:')
        for name in set([name for name, _, _ in process_dns_zone_file(options.file)]):
            print(name)

    if options.list_nameserver:
        print('Nameservers:')
        for name in set([name for name, _, _ in process_dns_zone_file(options.file)]):
            print(name)

    if options.record_type:
        print(f'Records of type {options.record_type}:')
        for name, type, value in process_dns_zone_file(options.file):
            if type == options.record_type:
                print(f"{name} {type} {value}")

    if options.ttl:
        print('TTL values:')
        for name, _, value in process_dns_zone_file(options.file):
            print(f"{name} {value}")

    if options.dnssec:
        print('DNSSEC public keys:')
        for name, _, _ in process_dns_zone_file(options.file):
            print(f"{name}")

if __name__ == '__main__':
    main()
