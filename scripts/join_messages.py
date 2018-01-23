"""joining messages and reqeust"""

from util import read_compressed_json_file, write_compressed_file, write_json_file


def join_successful_messages():
    requests = read_compressed_json_file(
        '../data/requests.json.gzip')["objects"]
    messages = read_compressed_json_file(
        '../data/messages.json.gzip')["objects"]

    data = []

    for r in requests:
        if r["resolution"] in ["successful", "partially_successful"]:
            request_url = f"https://fragdenstaat.de/api/v1/request/{r['id']}/"
            print(request_url)
            new_data =  [m for m in messages if m["is_response"] and m["request"] == request_url]
            data.extend(new_data)

    write_json_file('../data/suc_msg.json', data)


def join_failed_messages():
    requests = read_compressed_json_file(
        '../data/requests.json.gzip')["objects"]
    messages = read_compressed_json_file(
        '../data/messages.json.gzip')["objects"]

    data = []

    for r in requests:
        if r["status"] == "awaiting_classification":
            continue
        if r["resolution"] not in ["successful", "partially_successful"]:
            request_url = f"https://fragdenstaat.de/api/v1/request/{r['id']}/"
            print(request_url)
            new_data = [m for m in messages if m["is_response"]
                        and m["request"] == request_url]
            data.extend(new_data)

    write_json_file('../data/failed_msg.json', data)

def main():
    join_failed_messages()


if __name__ == '__main__':
    main()
