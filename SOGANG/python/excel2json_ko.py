import xlrd
import uuid
import simplejson as json
import math

# 카테고리 분류는 다음 링크를 참조했습니다.
# http://www.sogang.ac.kr/admin/index.html

# 연계전공 카테고리에서 '일본문화전공', '동아시아학전공'은 제외.
# 아래 링크에서는 '일본문화전공'과 '동아시아학 전공'이 연계전공으로 분류되어 있음
# https://www.sogang.ac.kr/bachelor/haksa/course01.html

# '아트&테크놀로지 전공'은 통폐합 된 '지식융합미디어학부'로 분류했습니다.
# '커뮤니케이션학 전공'은 통폐합 된 '지식융합미디어학부'로 분류했습니다.

# 종별(전필, 전선, 기교 등)의 분류가 없어서 일괄 null 처리 하였습니다.(대학요람 참조하는 방안으로 확인됨)

category1 = ["국제인문학부", "사회과학부", "지식융합학부", "지식융합미디어학부", "자연과학부", "공학부", "경제학부", "경영학부", "커뮤니케이션학부", "연계전공"]
category2 = [
    ["국어국문학전공", "사학전공", "철학전공", "종교학전공", "영미어문전공", "미국문화전공", "유럽문화전공", "독일문화전공", "프랑스문화전공", "중국문화전공", "일본문화전공"],
    ["사회학전공", "정치외교학전공", "심리학전공"],
    ["국제한국학전공", "아트&테크놀로지전공"],
    ["신문방송학전공", "미디어&엔터테인먼트전공", "아트&테크놀로지전공", "글로벌한국학전공"],
    ["수학전공", "물리학전공", "화학전공", "생명과학전공"],
    ["전자공학전공", "화공생명공학전공", "컴퓨터공학전공", "기계공학전공"],
    ["경제학전공"],
    ["경영학전공"],
    ["커뮤니케이션학전공"],
    ["교육문화연계전공", "공공인재 연계전공", "여성학 연계전공", "정치학/경제학/철학 연계전공", "스포츠미디어 연계전공", "바이오융합기술 연계전공", "스타트업연계전공", "융합소프트웨어연계전공", "한국발전과국제개발협력연계전공", "빅데이터사이언스연계전공", "인공지능연계전공", "한국사회문화연계전공"]
]

date_list = ["월", "화", "수", "목", "금", "토", "일"]

wb = xlrd.open_workbook('../xlsx/개설교과목정보(한글).xlsx')
sh = wb.sheet_by_index(0)

data_list = []

cnt = 0

def find_department(major):
    department = ''

    if major == '전인교육원':
        return '전인교육원'

    if major == '아트&테크놀로지전공':
        return '지식융합미디어학부'

    if major in category1 :
        return major

    for li in category2 :
        if major in li :
            department = category1[category2.index(li)]

    return department

def convert_year(year):
    year = year.replace("전학년", "")
    year = year.replace("학년", "")

    if year == '' :
        return None
    else :
        return year

def convert_credits(credits):
    if credits == '':
        return None
    else :
        return float(credits)

def convert_instructor(instructor):
    if instructor == '':
        return None
    else :
        return instructor

def convert_time_str(time_str):
    temp_dict = {}
    temp_list = []

    if time_str == '':
        return None

    date, times = time_str.split()
    date = date.split(",")
    times = times.split("~")

    start_time = float(times[0].split(":")[0]+"."+str(float(times[0].split(":")[1])/60)[2:4])
    end_time = float(times[1].split(":")[0]+"."+str(float(times[1].split(":")[1])/60)[2:4])

    temp_list.append({"start_time": start_time, "end_time": end_time})

    for element in date :
        element = str(date_list.index(element))
        temp_dict[element] = temp_list
    return temp_dict

for row_num in range(1, sh.nrows):
    dic = {}
    row_values = sh.row_values(row_num)

    # id
    dic['id'] = str(uuid.uuid5(uuid.NAMESPACE_URL, row_values[4].strip()+row_values[5]))

    # 단과대학(중분류) - string
    dic["department"] = find_department(row_values[3])

    # 전공(학과 등) - string
    dic["major"] = row_values[3]

    # 학년(이수 가능 학년) - string
    dic["year"] = convert_year(row_values[20])

    # 종별(전선, 전필, 기교 등) - string
    dic["classification"] = None

    # 학정번호-분반(-실습) - string
    dic["code"] = row_values[4] + "-" + row_values[5]

    # 학점 - float
    dic["credits"] = convert_credits(row_values[7])

    # 수업명 - string
    dic["title"] = row_values[6]

    # 교수명 - string
    dic["instructor"] = convert_instructor(row_values[10])

    # 강의 시간 - string
    dic["times_str"] = row_values[8]

    # 강의 시간 - dict
    dic["times"] = convert_time_str(row_values[8])

    # 강의실 - string
    dic["location"] = None

    #print(dic)
    #cnt += 1

    data_list.append(dic)

j = json.dumps(data_list, ensure_ascii=False, indent=4)

with open('../json/result_ko.json', 'w', encoding='UTF-8-sig') as f:
    f.write(j)