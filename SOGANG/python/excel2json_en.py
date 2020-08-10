import xlrd
import uuid
import simplejson as json

category1 = ["School of Humanities", "School of Social Sciences", "School of Intergrated Knowledge", "School of Media, Arts and Science", "School of Natural Sciences", "School of Engineering", "School of Economics", "Sogang Business School", "School of Communication", "Interdisciplinary Programs"]
category2 = [
    ["Korean Language and Literature", "History", "Philosophy", "Religious Studies", "British and American Language and Litera", "American Cultures", "European Languages and Cultures", "German Culture", "French Culture", "Chinese Culture", "Japanese Culture"],
    ["Sociology", "Political Science", "Psychology"],
    ["Korean Studies in English", "Art & Technology"],
    ["Journalism and Strategic Communication", "Media & Entertainment", "Art & Technology", "Global Korean Studies"],
    ["Mathematics", "Physics", "Chemistry", "Life Science"],
    ["Electronic Engineering", "Chemical and Biomolecular Engineering", "Computer Engineering", "Mechanical Engineering"],
    ["Economics"],
    ["Business Administration"],
    ["Communications"],
    ["Education Culture", "Public Leadership", "Gender Studies", "PEP(Political Science, Economics and Philosophy", "Sports Media", "Department of Biomedical Engineering", "Innovative Startup", "Convergence Software", "Korean development and International dev", "Big Data Science", "Artificial Intelligence", "Korean Society and Culture"]
]

date_list = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]

wb = xlrd.open_workbook('../xlsx/개설교과목정보(영문)_누락수정.xlsx')
sh = wb.sheet_by_index(0)

data_list = []

cnt = 0

def find_department(major):
    department = ''

    if major == 'School of General Education':
        return 'School of General Education'

    if major == 'Art & Technology' or major == 'Art&Technology':
        return 'School of Media, Arts and Science'

    if major in category1 :
        return major

    for li in category2 :
        if major in li :
            department = category1[category2.index(li)]

    if department == '':
        print(cnt)

    return department

def convert_year(year):
    year = year.replace("All grade(s)", "")
    year = year.replace(" grade(s)", "")
    year = year.replace(" grade(", "")

    #print(year)
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

def convert_time_str_to_location(time_str):
    if time_str == '':
        return None

    start = time_str.find("[")
    end = time_str.find("]")

    if start == -1 or end == -1:
        return None

    return time_str[start+1:end]


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
    dic["location"] = convert_time_str_to_location(row_values[8])

    #print(dic)
    cnt += 1

    data_list.append(dic)

j = json.dumps(data_list, ensure_ascii=False, indent=4)

with open('../json/result_en.json', 'w', encoding='UTF-8-sig') as f:
    f.write(j)