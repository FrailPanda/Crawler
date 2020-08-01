from os import listdir
from os.path import isfile, join
import json

# path = './json/korean/json/'
path = './json/english/json/'

file_list = [f for f in listdir(path) if isfile(join(path, f))]

cnt = 0
for i in range(len(file_list)):
    file_path = path + file_list[i]

    with open(file_path, 'r', encoding='UTF-8-sig') as f :
        data = json.load(f)

    cnt += len(data)

print(cnt)