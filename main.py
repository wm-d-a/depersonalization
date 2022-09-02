import csv
import os
import json


def json_deperson(buf):
    '''
    Функция обезличивания json
    :param buf: json в виде строки
    :return: Обезличенный json
    '''
    json_object = json.loads(buf)
    for obj in json_object:
        if type(json_object[str(obj)]) == str:
            json_object[str(obj)] = deperson(json_object[str(obj)])
        elif type(json_object[str(obj)]) == list:

            # Обезличиваем список
            for key, item in enumerate(json_object[str(obj)]):
                json_object[str(obj)][key] = deperson(str(item))
    try:
        del json_object['serial_number']
    except KeyError:
        pass
    result = json.dumps(json_object)
    return result


def deperson(buf):
    '''
    Функция обезличивания строки
    :param buf: строка
    :return: обезличенная строка
    '''
    result = ''
    for k, symbol in enumerate(buf):
        num = ord(symbol)
        if 0 <= num <= 47 or 58 <= num <= 64 or 91 <= num <= 96 or 123 <= num <= 127:
            result += symbol
        elif num == 122:
            result += chr(97)
        elif num == 90:
            result += chr(65)
        elif num == 57:
            result += chr(48)
        else:
            result += chr(num + 1)
    return result


def main(data):
    data = list(data)
    for i, row in enumerate(data):
        if i != 0:
            for j, item in enumerate(row):
                # j - номер столба таблицы
                if j == 2 or j == 8:
                    row[j] = deperson(item)
                if j == 5:
                    row[j] = json_deperson(item)
        data[i] = row
    return data


cur_dir = os.getcwd()

# Берем первый файл в директории с расширением .csv
file_name = [i for i in os.listdir(cur_dir) if '.csv' and 'query' in i][0]

with open(file_name, 'r') as csv_read:
    data = csv.reader(csv_read)
    data = main(data)
with open('new_query_result.csv', 'w', newline='') as csv_write:
    csv.writer(csv_write).writerows(data)
