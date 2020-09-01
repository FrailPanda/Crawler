import simplejson
import json
import uuid
import csv

def init():
    with open('../json/result.json', 'r', encoding="UTF-8-SIG") as json_file:
        json_data = json.load(json_file)

    with open('../xlsx/output.csv', 'r', encoding='UTF-8-sig', newline='') as f:
        reader = csv.reader(f)
        csv_data = list(reader)

    data_list = []

    for row in csv_data:
        for element in json_data:
            if element['code'].split("-")[0] == row[1] :
                dic = element
                dic['id'] = str(uuid.uuid4())
                dic['major'] = row[0]
                dic['title'] = row[2]

                data_list.append(dic)

    j = simplejson.dumps(data_list, ensure_ascii=False, indent=4)

    with open('../json/result_append.json', 'w', encoding='UTF-8-sig') as j_file:
        j_file.write(j)

if __name__ == "__main__":
    init()