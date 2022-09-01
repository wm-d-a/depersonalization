import csv
import os
import json


def json_deperson(buf):
    json_object = json.loads(buf)
    for obj in json_object:
        if type(json_object[str(obj)]) == str:
            json_object[str(obj)] = deperson(json_object[str(obj)])
        elif type(json_object[str(obj)]) == list:
            for key, item in enumerate(json_object[str(obj)]):
                json_object[str(obj)][key] = deperson(str(item))
    try:
        del json_object['serial_number']
    except KeyError:
        pass
    json_str = json.dumps(json_object)
    return json_str


def deperson(item):
    new_item = ''
    for k, symbol in enumerate(item):
        num = ord(symbol)
        if 0 <= num <= 64 or 91 <= num <= 96 or 123 <= num <= 127:
            new_item += symbol
        else:
            new_item += chr(num + 1)
    return new_item


def main(data):
    data = list(data)
    for i, row in enumerate(data):
        if i != 0:
            for j, item in enumerate(row):
                if j == 2 or j == 8:
                    row[j] = deperson(item)
                if j == 5:
                    row[j] = json_deperson(item)
        data[i] = row
    return data


cur_dir = os.getcwd()
file_name = [i for i in os.listdir(cur_dir) if '.csv' and 'query' in i][0]
with open(file_name, 'r') as csv_read:
    data = csv.reader(csv_read)
    data = main(data)
with open('new_query_result.csv', 'w', newline='') as csv_write:
    csv.writer(csv_write).writerows(data)
