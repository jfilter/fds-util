"""fetch resourses from FragDenStaat.de API"""

import json
import gzip
import os

import requests

DATA_DIR = '../data'

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

def init_data(filename):
    """init empty data"""
    write_compressed_file(filename, {'objects':[]})


def append_data(filename, new_data):
    """append data the json file"""

    data = read_compressed_json_file(filename)
    data['objects'].extend(new_data['objects'])
    write_compressed_file(filename, data)


def main(resource):
    """fetching requests"""
    filename = os.path.join(DATA_DIR, resource + 's.json.gzip')

    init_data(filename)
    next_url = 'https://fragdenstaat.de/api/v1/' + resource + '/?limit=300'

    while next_url:
        url = next_url
        r = requests.get(url)
        j = json.loads(r.content)
        append_data(filename, j)

        next_url = j['meta']['next']
        print("next_url", next_url)


if __name__ == '__main__':
    main('message')
    # main('request')
