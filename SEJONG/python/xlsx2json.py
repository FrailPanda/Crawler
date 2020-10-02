import xlrd
import uuid
import simplejson as json

department = [
    ["대양휴머니티칼리지", "인문과학대학", "사회과학대학", "경영대학", "호텔관광대학", "자연과학대학", "생명과학대학", "전자정보공학대학", "소프트웨어융합대학", "공과대학", "예체능대학", "법학부", "연계전공", "경영경제대학"],
    ["Daeyang Humanity College", "Liberal Art", "Social Sciences", "Business", "Hospitality and Tourism Management", "Natural Sciences", "Life Sciences", "Electronics and Information Engineering", "Software & Convergence Technology", "Engineering", "Arts and Physical Education", "Faculty of Law", "Interdisciplinary Programs", "Business and Economy"]
]

building = [
    ["집", "군", "광", "충", "영", "율", "애", "대", "용", "진", "모", "세", "새", "다", "이", "센", "동", "무"],
    ["Jip", "Gun", "Gwang", "Chung", "Yeong", "Yul", "Ae", "Dae", "Yong", "Jin", "Mo", "Se", "Happy Dormitory" "Da", "Yi", "Sen", "Dong", "Mu"]
]

date_list = ["월", "화", "수", "목", "금", "토", "일"]

def check_null_value(item):
    if item == '':
        return None
    else:
        return item

def convert_time_str2english(time):
    if time == None:
        return None

    time = time.replace("월", "Mon")
    time = time.replace("화", "Tue")
    time = time.replace("수", "Wed")
    time = time.replace("목", "Thu")
    time = time.replace("금", "Fri")
    time = time.replace("토", "Sat")
    time = time.replace("일", "Sun")

    return time

def convert_location(location):
    if location == '':
        return None

    if "글로벌" in location:
        return location.replace("글로벌", "Global")

    if "Lab" in location:
        return location

    if location == "새실기실":
        return "Happy Dormitory Practical Room"

    if location == "대양홀강당":
        return "Daeyang Hall Auditorium"

    if location == "학대공연장":
        return "Students Hall"

    result = ''

    if "," in location:
        location = location.split(",")
        result += building[1][building[0].index(location[0][0])]
        result += ' '
        result += location[0][1:]

        result += '/'

        result += building[1][building[0].index(location[1][0])]
        result += ' '
        result += location[1][1:]

    else :
        result += building[1][building[0].index(location[0])]
        result += ' '
        result += location[1:]

    return result

def convert_time_str2dict(time):
    if time == '' :
        return None

    result = {}

    if ',' in time :
        date = []
        time = time.split(",")

        date_and_time = [[], [], [], [], [], [], []]

        time[0] = time[0].split()
        for i in range(len(time[0])-1):
            date.append(time[0][i])

        time[0] = time[0][-1]
        time[0] = time[0].split("~")

        start_time = float(time[0][0].split(":")[0]) + float(time[0][0].split(":")[1]) / 60
        end_time = float(time[0][1].split(":")[0]) + float(time[0][1].split(":")[1]) / 60

        for d in date:
            d_index = date_list.index(d)
            date_and_time[d_index].append({"start_time": start_time, "end_time": end_time})

        # ---

        date = []

        time[1] = time[1].split()
        for i in range(len(time[1])-1):
            date.append(time[1][i])

        time[1] = time[1][-1]
        time[1] = time[1].split("~")

        start_time = float(time[1][0].split(":")[0]) + float(time[1][0].split(":")[1]) / 60
        end_time = float(time[1][1].split(":")[0]) + float(time[1][1].split(":")[1]) / 60

        for d in date:
            d_index = date_list.index(d)
            date_and_time[d_index].append({"start_time": start_time, "end_time": end_time})

        for i in range(len(date_and_time)):
            if date_and_time[i] :
                result[str(i)] = date_and_time[i]

    else:
        date = []
        time = time.split()
        for i in range(len(time)-1):
            date.append(time[i])

        time = time[-1]
        time = time.split("~")

        start_time = float(time[0].split(":")[0]) + float(time[0].split(":")[1])/60
        end_time = float(time[1].split(":")[0]) + float(time[1].split(":")[1]) / 60

        for d in date:
            d_index = str(date_list.index(d))
            result[d_index] = [{"start_time" : start_time, "end_time":end_time}]

    return result




wb = xlrd.open_workbook('../xlsx/2020-2.xlsx')
sh = wb.sheet_by_index(0)

data_list = []

for row_num in range(1, sh.nrows):
    row_values = sh.row_values(row_num)

    dic = {}

    # id
    dic['id'] = str(uuid.uuid4())

    # code
    dic['code'] = row_values[3]+'-'+row_values[4]

    # title
    dic['title'] = row_values[25]

    # instructor
    dic['instructor'] = check_null_value(row_values[31])

    # department
    # 영문으로 번역해야됨
    # 번역 완료(학교 홈페이지 참조)
    dic['department'] = department[1][department[0].index(row_values[1])]

    # major
    # 신설 전공에 대해서는 영문 정보가 없음
    # 자체 번역하여 수정
    dic['major'] = row_values[22]

    # classification
    dic['classification'] = row_values[26]

    # year
    dic['year'] = str(int(row_values[27]))

    # credits
    dic['credits'] = float(row_values[28])

    # location
    dic['location'] = convert_location(row_values[13])

    # times_str
    dic['times_str'] = convert_time_str2english(check_null_value(row_values[12]))

    # times
    dic['times'] = convert_time_str2dict(row_values[12])

    data_list.append(dic)

j = json.dumps(data_list, ensure_ascii=False, indent=4)

with open('../json/result.json', 'w', encoding='UTF-8-sig') as f:
    f.write(j)