def translate(time_str):
    if not time_str :
        return None

    time_str = time_str.replace("월", "Mon ")
    time_str = time_str.replace("화", "Tue ")
    time_str = time_str.replace("수", "Wed ")
    time_str = time_str.replace("목", "Thu ")
    time_str = time_str.replace("금", "Fri ")
    time_str = time_str.replace("토", "Sat ")

    return time_str

def time_dict(time):
    if time is None :
        return None

    date_list = ["월", "화", "수", "목", "금", "토", "일"]

    time = time.replace(" ", "")

    time = time.replace("월", " 월 ")
    time = time.replace("화", " 화 ")
    time = time.replace("수", " 수 ")
    time = time.replace("목", " 목 ")
    time = time.replace("금", " 금 ")
    time = time.replace("토", " 토 ")

    time = time.split()

    temp = [[],[],[],[],[],[]]
    for element in time:
        if element in date_list:
            date = element
            continue
        else:
            times = element[:element.find('/')].split(',')

            for i in range(len(times)):
                times[i] = int(times[i])

            start_time = float(times[0] + 8)
            end_time = float(times[-1] + 9)

            temp[date_list.index(date)].append({"start_time":start_time, "end_time":end_time})
            # print(date, times)

    result = {}

    for i in range(len(temp)):
        if temp[i]:
            result[str(i)] = temp[i]
    return result

def convert_location(time):
    if time is None :
        return None

    date_list = ["월", "화", "수", "목", "금", "토", "일"]

    time = time.replace("월", " 월 ")
    time = time.replace("화", " 화 ")
    time = time.replace("수", " 수 ")
    time = time.replace("목", " 목 ")
    time = time.replace("금", " 금 ")
    time = time.replace("토", " 토 ")

    time = time.split()
    result = ''

    for element in time :
        if element in date_list :
            date = element
            continue
        else :
            times = element[:element.find('/')]
            location = element[element.find('/')+1:]
            location = location.replace(",", "")
            location = location.replace(".", "/")

            result += location + '+'

    result = list(set(result.split("+")))
    temp = ''
    for element in result:
        if element == '':
            continue
        else :
            temp += element + ', '

    result = temp[:-2]
    return result