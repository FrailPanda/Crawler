import custom_module_stony
import simplejson as json
import uuid
import xlrd

def check_null_value(item):
    if item == '' :
        return None
    else :
        return item

def init():
    wb = xlrd.open_workbook('../xlsx/Stony Brook 수작업.xlsx')
    sh = wb.sheet_by_index(0)

    wb_datemode = wb.datemode
    data_list = []

    temp_time_str = ''
    temp_location = ''

    for row_num in range(1, sh.nrows):
        row_value = sh.row_values(row_num)

        if row_value[8] == '' :
            y, M, d, h, m, s = xlrd.xldate_as_tuple(row_value[11], wb_datemode)
            start_time = "{0}:{1}".format(h, m)

            y, M, d, h, m, s = xlrd.xldate_as_tuple(row_value[12], wb_datemode)
            end_time = "{0}:{1}".format(h, m)

            temp_time_str = row_value[10] + ' ' + start_time + '~' + end_time + '/'
            temp_location = row_value[13] + '/'

            continue

        dic = {}

        # id
        dic['id'] = str(uuid.uuid4())

        # code
        # dic['code'] = row_value[]

        # instructor
        dic['instructor'] = row_value[14]

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
        dic['credits'] = float(row_value[8]) if isinstance(row_value[8], float) else None

        # time_str
        y, M, d, h, m, s = xlrd.xldate_as_tuple(row_value[11], wb_datemode)
        start_time = "{0}:{1}".format(h, m)

        y, M, d, h, m, s = xlrd.xldate_as_tuple(row_value[12], wb_datemode)
        end_time = "{0}:{1}".format(h, m)

        dic['time_str'] = temp_time_str + row_value[10] + ' ' + start_time + '~' + end_time

        if "APPT" in dic['time_str'] or "HTBA" in dic['time_str'] :
            dic['time_str'] = None

        # times
        dic['times'] = custom_module_stony.times(dic['time_str'])

        # location
        dic['location'] = check_null_value(temp_location + row_value[13])

        data_list.append(dic)

        temp_time_str = ''
        temp_location = ''


    j = json.dumps(data_list, ensure_ascii=False, indent=4)

    with open('../json/result.json', 'w', encoding='UTF-8-sig') as f:
        f.write(j)

if __name__ == "__main__":
    init()