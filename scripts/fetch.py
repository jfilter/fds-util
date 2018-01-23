"""fetch resourses from FragDenStaat.de API"""

import json
import os

import requests

from util import read_compressed_json_file, write_compressed_file

DATA_DIR = '../data'

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
