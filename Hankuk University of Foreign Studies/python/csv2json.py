# -*- coding: utf-8 -*-

import simplejson as json
import uuid
import csv

date_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def convert_time_str(time):
    if time == '()':
        return None

    time = time.split('\n')
    time = time[1]
    time = time[1:-1]

    result = ''
    flag = True
    for i in range(len(time)):
        if time[i] == '(':
            flag = False

        if flag :
            result += time[i]

        if time[i] == ')':
            flag = True

    return result[:-1]

def convert_location(time):
    if time == '()':
        return None

    time = time.split('\n')
    time = time[0]

    temp_list = []
    temp_str = ''

    for i in range(len(time)):
        if time[i-1] == '(':
            while time[i] != ')':
                temp_str += time[i]
                i += 1
            temp_list.append(temp_str)
            temp_str = ''

    temp_str = ''

    if len(temp_list) == 1:
        if temp_list[0] == '-' or temp_list[0] == ' ':
            return None
        else :
            return temp_list[0]
    else :
        for element in temp_list:
            if element == '-' or element == ' ':
                temp_str = temp_str + 'None' + '/'
            else :
                temp_str = temp_str + element + '/'

        temp_str = temp_str[:-1]
        return temp_str

def convert_title(title):
    if '\n' not in title:
        return title

    title = title.split('\n')
    title = title[1]
    title = title[1:-1]

    return title

def convert_instructor(instructor):
    if instructor == '(-)':
        return None

    instructor = instructor.split("\n")

    if len(instructor)==1 :
        return instructor[0]

    else :
        if instructor[1] == "(-)":
            return instructor[0]
        if isEnglish(instructor[0]) :
            return instructor[0]
        else:
            return instructor[1][1:-1]

def time_str2json_1(time):
    # 하루에 두번 수업하는 과목들에 대해서는 수작업
    # print(time)
    # if time == [1, '1', '2', 1, '10'] :
    #    return {"1":[{"start_time" : 9.0, "end_time" : 11.0}, {"start_time":18.0, "end_time":19.0}]}
    return None

def time_str2json_2(time):
    for i in range(len(time)):
        if isinstance(time[i], int):
            time[i] = date_list[time[i]]

    li = []
    l = []

    for i in range(len(time)):
        l.append(time[i])

        if time[i].isdigit() and i != len(time) - 1:
            if time[i + 1] in date_list:
                li.append(l)
                l = []

    # 위 반복문을 거친 후, l이 공백 리스트가 아닌경우
    if l:
        # append()
        li.append(l)

    temp_result = {}

    for element in li :
        element[0] = date_list.index(element[0])

        start_time = float(element[1])+8
        end_time = float(element[-1])+9

        temp_result[str(element[0])] = [{"start_time" : start_time, "end_time" : end_time}]

    return temp_result

def convert_time(time):
    if time == None :
        return None

    temp_cnt = 0

    time = time.split()
    for i in range(len(time)):
        if time[i] in date_list :
            time[i] = date_list.index(time[i])

    for i in range(len(time)):
        if type(time[i]) == type(1):
            temp_cnt += 1

    li = []

    if temp_cnt >= 2:
        for i in range(len(time)):
            if type(time[i]) == type(1):
                li.append(time[i])

    flag = 0

    for i in range(len(li)):
        for j in range(i):
            if li[i] == li[j]:
                flag = 1
                break

    if flag :
        return time_str2json_1(time)

    else :
        return time_str2json_2(time)

def convert_year(year):
    if year == '':
        return None

    return str(year)

def init():
    with open('../csv/output.csv', 'r', encoding='UTF-8-sig', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    # json result
    result = []

    for i in range(1, len(data)):
        dic = dict()

        # id - random uuid
        dic["id"] = str(uuid.uuid4())

        # 단과대학(중분류) - string
        dic["department"] = data[i][0]

        # 전공(학과 등) - string
        if dic["department"] == "Practical foreign language/Liberal arts":
            dic["major"] = data[i][1].replace(" ", "").replace("\n", "")
        else :
            dic["major"] = data[i][1].replace("Department of ", "")


        # 학년(이수 가능 학년) - int
        dic["year"] = convert_year(data[i][6])

        # 종별(전선, 전필, 기교 등) - string
        dic["classification"] = data[i][5]

        # 학정번호-분반(-실습) - string
        dic["code"] = data[i][2]

        # 학점 - float
        dic["credits"] = float(data[i][7])

        # 수업명 - string
        dic["title"] = convert_title(data[i][3])

        # 교수명 - string
        dic["instructor"] = convert_instructor(data[i][4])

        # 강의 시간 - string
        dic["times_str"] = convert_time_str(data[i][8])

        # 강의 시간 - dict
        dic["times"] = convert_time(dic["times_str"])

        # 강의실 - string
        dic["location"] = convert_location(data[i][8])

        result.append(dic)

    j = json.dumps(result, ensure_ascii=False, indent=4)
    with open('../json/result.json', 'w', encoding='UTF-8-sig') as file:
        file.write(j)
    file.close()

if __name__ == "__main__":
    init()