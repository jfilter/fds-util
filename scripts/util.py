"""util for IO"""

import gzip
import json


def read_compressed_json_file(filename):
    """reads in compress JSON file and returns dict"""
    data = None
    with gzip.GzipFile(filename, 'r') as fin:
        json_bytes = fin.read()
        json_str = json_bytes.decode('utf-8')
        data = json.loads(json_str)
    return data

def write_compressed_file(filename, data):
    """write dict to compress JSON file"""

    with gzip.GzipFile(filename, 'w', compresslevel=5) as fout:
        json_str = json.dumps(data) + '\n'
        json_bytes = json_str.encode('utf-8')
        fout.write(json_bytes)

def write_json_file(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
