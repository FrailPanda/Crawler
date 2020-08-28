from timestr2dict import time_dict

import simplejson as json
import uuid
import xlrd

def init():
    wb = xlrd.open_workbook('../xlsx/2020-2_20200814.xlsx')
    sh = wb.sheet_by_index(1)

    data_list = []

    for row_num in range(1, sh.nrows):
        row_value = sh.row_values(row_num)

        dic = {}

        # id
        dic['id'] = str(uuid.uuid4())

        # code
        dic['code'] = str(row_value[2]).split('.')[0]

        # instructor
        dic['instructor'] = row_value[9].split()[0]

        # department

        # major

        # classification

        # year

        # credits

        # location

        # time_str

        # times
        data_list.append(dic)

    j = json.dumps(data_list, ensure_ascii=False, indent=4)

    with open('../json/result_english_course.json', 'w', encoding='UTF-8-sig') as f:
        f.write(j)


if __name__ == "__main__":
    init()