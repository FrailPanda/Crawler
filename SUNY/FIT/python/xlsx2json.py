import custom_module_FIT
import simplejson as json
import uuid
import xlrd

def check_null_value(item):
    if item == '' :
        return None
    else :
        return item

def init():
    wb = xlrd.open_workbook('../xlsx/FIT 수작업.xlsx')
    sh = wb.sheet_by_index(0)

    wb_datemode = wb.datemode
    data_list = []

    temp_time_str = ''

    for row_num in range(1, sh.nrows):
        row_value = sh.row_values(row_num)

        if row_value[6] == '' :
            y, M, d, h, m, s = xlrd.xldate_as_tuple(row_value[9], wb_datemode)
            start_time = "{0}:{1}".format(h, m)

            y, M, d, h, m, s = xlrd.xldate_as_tuple(row_value[10], wb_datemode)
            end_time = "{0}:{1}".format(h, m)

            temp_time_str = row_value[8] + ' ' + start_time + '~' + end_time + '/'

            continue

        dic = {}

        # id
        dic['id'] = str(uuid.uuid4())

        # code
        # dic['code'] = row_value[]

        # instructor
        dic['instructor'] = row_value[12]

        # department
        dic['department'] = row_value[0]

        # title
        dic['title'] = row_value[4]

        # major
        dic['major'] = row_value[2]

        # classification
        dic['classification'] = None

        # year
        dic['year'] = None

        # credits
        dic['credits'] = float(row_value[6]) if isinstance(row_value[6], float) else None

        # time_str
        y, M, d, h, m, s = xlrd.xldate_as_tuple(row_value[9], wb_datemode)
        start_time = "{0}:{1}".format(h, m)

        y, M, d, h, m, s = xlrd.xldate_as_tuple(row_value[10], wb_datemode)
        end_time = "{0}:{1}".format(h, m)

        dic['time_str'] = temp_time_str + row_value[8] + ' ' + start_time + '~' + end_time
        print(dic['time_str'])
        # times
        dic['times'] = custom_module_FIT.times(dic['time_str'])

        # location
        dic['location'] = check_null_value(row_value[11])

        data_list.append(dic)

        temp_time_str = ''


    j = json.dumps(data_list, ensure_ascii=False, indent=4)

    with open('../json/result.json', 'w', encoding='UTF-8-sig') as f:
        f.write(j)

if __name__ == "__main__":
    init()