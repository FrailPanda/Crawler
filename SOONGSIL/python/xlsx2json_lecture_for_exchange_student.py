from timestr2dict import time_dict

import simplejson as json
import uuid
import xlrd

def convert_location(time):
    result = ''
    time = time.split()

    temp = []
    for element in time :
        if '(' in element :
            temp.append(element[1:-1])

    if len(temp) == 1:
        result = temp[0].split('-')[0]
        if result is not '':
            return result
        else :
            return None

    for element in temp:
        element = element.split('-')[0]
        if element == '':
            continue
        result = result + element + '/'

    if result == '':
        return None
    else :
        return result[:-1]

def init():
    wb = xlrd.open_workbook('../xlsx/2020-2_20200814.xlsx')
    sh = wb.sheet_by_index(0)

    data_list = []

    for row_num in range(1, sh.nrows):
        row_value = sh.row_values(row_num)

        dic = {}

        # id
        dic['id'] = str(uuid.uuid4())

        # code
        dic['code'] = str(row_value[1]).split('.')[0]

        # title
        dic['title'] = row_value[3]

        # instructor
        dic['instructor'] = row_value[8].split()[0]

        # department
        dic['department'] = row_value[3]

        # major
        dic['major'] = row_value[3]

        # classification
        dic['classification'] = None

        # year
        dic['year'] = None

        # credits
        dic['credits'] = 3.0

        # location
        dic['location'] = convert_location(row_value[6])

        # times_str
        dic['times_str'] = row_value[6]

        # times
        #

        data_list.append(dic)

    j = json.dumps(data_list, ensure_ascii=False, indent=4)

    with open('../json/result_lecture_for_exchange_student.json', 'w', encoding='UTF-8-sig') as f:
        f.write(j)

if __name__ == "__main__":
    init()