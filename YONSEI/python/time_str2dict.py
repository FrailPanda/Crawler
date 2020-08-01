import csv

path = '../csv/korean/korean_output.csv'

with open(path, 'r', encoding='UTF-8-sig', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

header = data[0]
date_list = ["월", "화", "수", "목", "금", "토", "일"]


def print_if_b_is_not_c(origin, a, b, c, result) :
    global cnt
    if b != c :
        print(origin)
        print("====>", a)
        print("====>", b)
        print("====>", c)
        print("====>", result)
        print()

def isSymmetric(str) :
    return str[:int((len(str)-1)/2)] == str[int((len(str)-1)/2+1):]

def sort_list_by_date(temp_list) :
    li = []
    l = []

    for i in range(len(temp_list)) :
        l.append(temp_list[i])

        if temp_list[i].isdigit() and i != len(temp_list)-1:
            if temp_list[i + 1] in date_list :
                li.append(l)
                l = []
    if l:
        li.append(l)

    for i in range(len(li)) :
        li[i][0] = date_list.index(li[i][0])

    li.sort(key=lambda x:x[0])

    for i in range(len(li)) :
        li[i][0] = date_list[li[i][0]]

    a = []

    for i in li :
        for j in i:
            a.append(j)

    # print("====>", li)
    # print("====>", a)

    return a

def sort_and_delete_duplication_time(temp_list):
    li = []
    l = []

    for i in range(len(temp_list)):
        l.append(temp_list[i])

        if temp_list[i].isdigit() and i != len(temp_list) - 1:
            if temp_list[i + 1] in date_list:
                li.append(l)
                l = []
    if l:
        li.append(l)

    for i in range(len(li)):
        li[i][0] = date_list.index(li[i][0])

    for i in li :
        for j in range(1,len(i)):
            i[j] = int(i[j])
        i[1:] = sorted(i[1:])

        for j in range(1, len(i)):
            i[j] = str(i[j])

        for j in range(1, len(i)):
            if i[j] in i[1:j] :
                i[j] = ' '

        i[0] = date_list[i[0]]

    a = []

    for i in li:
        for j in i:
            if j != ' ':
                a.append(j)

    return a

def check_continuous_time(temp_list):
    li = []
    l = []

    for i in range(len(temp_list)):
        l.append(temp_list[i])

        if temp_list[i].isdigit() and i != len(temp_list) - 1:
            if temp_list[i + 1] in date_list:
                li.append(l)
                l = []
    if l:
        li.append(l)

    flag = True

    for i in li :
        for j in range(1, len(i)-1):
            if int(i[j+1]) - int(i[j]) != 1 :
                flag = False
                break

    return flag

for i in range(1, len(data)):
    original_str = data[i][16]
    temp_str = data[i][16]

    if original_str.strip() == '':
        continue

    if isSymmetric(original_str):
        temp_str = original_str[:int((len(original_str)-1)/2)]

    elif isSymmetric(original_str.replace("(", ",").replace(")", "")):
        temp_str = original_str[:int((len(original_str)-1)/2)]

    else :
        pass

    for ch in temp_str :
        if ch in date_list:
            temp_str = temp_str.replace(ch, ch+" ")

    temp_str = temp_str.replace("/", " ")
    temp_str = temp_str.replace("(", " ")
    temp_str = temp_str.replace(")", " ")
    temp_str = temp_str.replace(",", " ")
    #print("====>", temp_str)

    temp_list = temp_str.split() # 여기까진 이상없음
    #print("====>", temp_list)

    temp_list = sort_list_by_date(temp_list)

    for j in range(len(temp_list)) :
        for k in range(j) :
            if temp_list[j] == temp_list[k] and temp_list[j] in date_list :
                temp_list[j] = ' '
    # print("====>", temp_list)

    for j in temp_list :
        if j == ' ' :
            index = temp_list.index(j)
            del temp_list[index]
    # print("====>", temp_list)

    temp_list = sort_and_delete_duplication_time(temp_list)
    # print("====>", temp_list)

    if check_continuous_time(temp_list) :
        # print(temp_list)
        pass
    else :
        # 하루에 두 번 수업하는 경우
        print(temp_list)
        #pass

    result = []
    for j in temp_list:
        result.append(j)
