def times(time_str):
    if time_str is None :
        return None

    result = {}
    date_list = ["M", "TU", "W", "TH", "F"]
    temp_list = [[], [], [], [], []]

    time_str = time_str.split("/")

    for element in time_str :
        dates = element.split(" ")[0]
        times = element.split(" ")[1]

        dates = dates.replace("M", "M ")
        dates = dates.replace("T", "TU ")
        dates = dates.replace("W", "W ")
        dates = dates.replace("R", "TH ")
        dates = dates.replace("F", "F ")

        dates = dates.split()

        start_time = float(times.split("~")[0].split(":")[0]) + float(times.split("~")[0].split(":")[1])/60
        end_time = float(times.split("~")[1].split(":")[0]) + float(times.split("~")[1].split(":")[1]) / 60

        for date in dates :
            temp_list[date_list.index(date)].append({"start_time" : round(start_time, 2), "end_time" : round(end_time, 2)})

    for i in range(5):
        if temp_list[i] :
            result[str(i)] = temp_list[i]
    return result