import simplejson as json
import uuid
from os import listdir
from os.path import isfile, join
import csv

date_list = ["월", "화", "수", "목", "금", "토", "일"]

def checkNullStr(item):
    _item = item.strip()
    if _item == '':
        return None
    else:
        return _item

# dic["times"] 처리 함수
def isSymmetric(str):
    return str[:int((len(str) - 1) / 2)] == str[int((len(str) - 1) / 2 + 1):]

def sort_list_by_date(temp_list):
    li = []
    l = []

    # 요일 기준으로 묶음
    # ex. ["월", "4", "5", "화", "4", "5", "월", "2", "3"]
    # -> [["월", "4", "5"], ["화", "4", "5"], ["월", "2", "3"]]
    for i in range(len(temp_list)):
        l.append(temp_list[i])

        if temp_list[i].isdigit() and i != len(temp_list) - 1:
            if temp_list[i + 1] in date_list:
                li.append(l)
                l = []

    # 위 반복문을 거친 후, l이 공백 리스트가 아닌경우
    if l:
        li.append(l)

    # li의 각 요소의 첫 번째 요소(요일)를 숫자로 변환
    # ex. "월" -> 0
    for i in range(len(li)):
        li[i][0] = date_list.index(li[i][0])

    # 요일 값 기준으로 리스트 정렬
    li.sort(key=lambda x: x[0])

    # 요일 값을 다시 string으로 변환
    for i in range(len(li)):
        li[i][0] = date_list[li[i][0]]

    result = []
    for element in li:
        for e in element:
            result.append(e)

    return result

def sort_and_delete_duplication_time(temp_list):
    li = []
    l = []

    # 요일 기준으로 묶음
    # ex. ["월", "4", "5", "화", "4", "5", "월", "2", "3"]
    # -> [["월", "4", "5"], ["화", "4", "5"], ["월", "2", "3"]]
    for i in range(len(temp_list)):
        l.append(temp_list[i])

        if temp_list[i].isdigit() and i != len(temp_list) - 1:
            if temp_list[i + 1] in date_list:
                li.append(l)
                l = []
    # 위 반복문을 거친 후, l이 공백 리스트가 아닌경우
    if l:
        # append()
        li.append(l)

    # li의 각 요소의 첫 번째 요소(요일)를 숫자로 변환
    # ex. "월" -> 0
    for i in range(len(li)):
        li[i][0] = date_list.index(li[i][0])

    # 요일 값 뒤의 요소(시간)를 정렬
    for element in li :
        # 시간(문자) -> 시간(숫자)
        for i in range(1, len(element)):
            element[i] = int(element[i])

        # 정렬
        element[1:] = sorted(element[1:])

        # 정렬 후, 시간(숫자)->시간(문자)
        for i in range(1, len(element)):
            element[i] = str(element[i])

        # 시간대 중복제거
        for i in range(1, len(element)):
            if element[i] in element[1:i] :
                element[i] = ''

        # 요일(숫자)-> 요일(문자)
        element[0] = date_list[element[0]]

    result = []

    for element in li:
        for e in element:
            if e != '':
                result.append(e)

    return result

def check_continuous_time(temp_list):
    li = []
    l = []

    # 요일 단위로 이중리스트로 변환 작업.
    # 다른 함수들에서도 볼 수 있음 -> 모듈화 가능 / 추후 수정 혹은 유지
    for i in range(len(temp_list)):
        l.append(temp_list[i])

        if temp_list[i].isdigit() and i != len(temp_list) - 1:
            if temp_list[i + 1] in date_list:
                li.append(l)
                l = []
    if l:
        li.append(l)

    flag = True

    for element in li :
        for i in range(1, len(element)-1):
            # 만약 시간대가 연속하지 않는다면
            if int(element[i+1]) - int(element[i]) != 1 :
                flag = False
                break
    return flag

def time_str2json_1(temp_list):
    result = {}
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

    for element in li :
        # 요일(문자) -> 요일(숫자)
        element[0] = date_list.index(element[0])

        time = []
        start_time = float(int(element[1])+8)
        finish_time = float(int(element[-1])+9)

        time.append({"start_time" : start_time, "finish_time" : finish_time})

        result[element[0]] = time

    return result

def time_str2json_2(temp_list) :
    result = {}
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

    for element in li :
        element[0] = date_list.index(element[0])

        # 중복인 시간대를 처리하기 위해 time_list에 time을 append() 해줌
        time_list = []
        time = []

        for i in range(1, len(element)):
            time.append(element[i])
            if i == len(element)-1 :
                break
            if int(element[i+1])-int(element[i]) != 1 :
                time_list.append(time)
                time = []
        time_list.append(time)

        # time_list 리스트의 요소였던 time 리스트 -> value 값(list)으로 재사용
        time = []

        for e in time_list :
            start_time = float(int(e[0]) + 8)
            finish_time = float(int(e[-1]) + 9)

            time.append({"start_time": start_time, "finish_time": finish_time})

        result[element[0]] = time

    return result


def convertTime(time) :
    # 중간중간 check 하기 위해 original_str 변수 생성 했습니다
    original_str = time

    # 문자열 처리는 temp_str
    temp_str = time
    
    # 강의 시간이 나오지 않은 경우
    if original_str.strip() == '':
        # null
        return None
    
    # 강의 시간이 대칭인 경우(ex. 화4,5/화4,5), 절반으로 slicing
    if isSymmetric(original_str):
        temp_str = original_str[:int((len(original_str) - 1) / 2)]
    
    # "("을 ","로, ")"을 공백으로 처리한 결과가 대칭인 경우(ex. 화4,5(화4,5)), 절반으로 slicing 
    elif isSymmetric(original_str.replace("(", ",").replace(")", "")):
        temp_str = original_str[:int((len(original_str) - 1) / 2)]

    else:
        pass
    
    # 요일 뒤에 공백 추가 -> 공백 기준으로 split() 하기 위함
    for ch in temp_str:
        if ch in date_list:
            temp_str = temp_str.replace(ch, ch + " ")
    
    # 특수문자들 공백으로 변환
    temp_str = temp_str.replace("/", " ")
    temp_str = temp_str.replace("(", " ")
    temp_str = temp_str.replace(")", " ")
    temp_str = temp_str.replace(",", " ")
    # print("====>", temp_str)

    # 여기까진 이상없음
    # 공백 기준으로 split()
    # "월 4 5 화 4 5 월 2 3" -> ["월", "4", "5", "화", "4", "5", "월", "2", "3"]
    temp_list = temp_str.split()
    # print("====>", temp_list)
    
    # 요일 단위로 정렬
    # ex. ["월", "4", "5", "화", "4", "5", "월", "2", "3"]
    # -> ["월", "2", "3", "월", "4", "5", "화", "4", "5"]
    temp_list = sort_list_by_date(temp_list)

    # 요일 값 중복 제거 -> 해당 요일 이전에 같은 요일이 있는 경우 공백으로 변환
    for i in range(len(temp_list)):
        for j in range(i):
            if temp_list[i] == temp_list[j] and temp_list[i] in date_list:
                temp_list[i] = ' '
    # print("====>", temp_list)

    # 위 과정을 거친 후, 공백인 요소를 delete
    for element in temp_list:
        if element == ' ':
            index = temp_list.index(element)
            del temp_list[index]
    # print("====>", temp_list)

    # 시간대 정렬 후 시간대가 중복이면 delete
    # ex. ["월", "2", "3", "2"] -> ["월", "2", "3"]
    temp_list = sort_and_delete_duplication_time(temp_list)
    # print("====>", temp_list)

    # 하루에 두 번 이상 진행하는 과목이 8개가 있어서, 해당부분 처리.
    # check_continuous_time : 시간대가 연속인지 체크
    # 연속할 경우 True, 연속하지 않을 경우 False return
    # json 변환 작업(정확히는 딕셔너리로 변환 작업)
    if check_continuous_time(temp_list):
        result = time_str2json_1(temp_list)
    else:
        result = time_str2json_2(temp_list)

    return result

def init():
    cnt = 0
    folder_path = '../csv/korean/group/'
    file_list = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

    for i in range(len(file_list)):
        file_path = folder_path + file_list[i]

        with open(file_path, 'r', encoding='UTF-8-sig', newline='') as f :
            reader = csv.reader(f)
            data = list(reader)
        
        # json result
        result = []

        for j in range(1, len(data)):
            dic = dict()

            # id - string
            dic["id"] = str(uuid.uuid5(uuid.NAMESPACE_URL, data[j][8].strip()))

            # 단과대학(중분류) - string
            dic["department"] = data[j][0]

            # 전공(학과 등) - string
            dic["major"] = data[j][1]

            # 학년(이수 가능 학년) - int
            dic["year"] = checkNullStr(data[j][5])

            # 종별(전선, 전필, 기교 등) - string
            dic["classification"] = data[j][6]

            # 학정번호-분반(-실습) - string
            dic["code"] = data[j][8].strip()

            # 학점 - float
            dic["credits"] = float(data[j][9])

            # 수업명 - string
            dic["title"] = data[j][10]

            # 교수명 - string
            dic["instructor"] = checkNullStr(data[j][15])

            # 강의 시간 - string
            dic["times_str"] = checkNullStr(data[j][16])

            # 강의 시간 - dict
            dic["times"] = convertTime(data[j][16])

            # 강의실 - string
            dic["location"] = checkNullStr(data[j][17])

            result.append(dic)
            cnt += 1

        j = json.dumps(result, ensure_ascii=False, indent=4)
        with open('../json/korean/' + file_list[i][:-4] + '.json', 'w', encoding='UTF-8-sig') as file:
            file.write(j)
        file.close()
        print(file_list[i] + " : done")

    print(cnt)

if __name__ == "__main__" :
    init()