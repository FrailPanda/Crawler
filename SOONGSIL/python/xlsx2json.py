from soongsil_modules import time_dict, convert_department_ko, translate_major, convert_year, convert_location, check_null_value, convert_time

import simplejson as json
import uuid
import xlrd

def init():
    wb = xlrd.open_workbook('../xlsx/2020-2_20200814.xlsx')
    sh = wb.sheet_by_index(2)

    data_list = []

    for row_num in range(1, sh.nrows):
        row_value = sh.row_values(row_num)

        dic = {}

        # id
        dic['id'] = str(uuid.uuid4())

        # code
        dic['code'] = str(row_value[2]).split('.')[0]

        # instructor
        dic['instructor'] = ' '.join(row_value[9].split()[:-1]) if check_null_value(row_value[9]) else None

        # department
        dic['department'] = convert_department_ko(row_value[4])

        # major
        dic['major'] = translate_major(row_value[4])

        # title
        dic['title'] = row_value[6]

        # classification
        dic['classification'] = None

        # year
        dic['year'] = convert_year(row_value[12])

        # credits
        dic['credits'] = float(row_value[3])

        # location
        dic['location'] = convert_location(check_null_value(row_value[7]))

        # time_str
        dic['time_str'] = convert_time(check_null_value(row_value[7]))

        # times
        dic['times'] = time_dict(dic['time_str'])


        data_list.append(dic)

    j = json.dumps(data_list, ensure_ascii=False, indent=4)

    with open('../json/result.json', 'w', encoding='UTF-8-sig') as f:
        f.write(j)

if __name__ == "__main__":
    init()