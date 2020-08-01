import csv

# rows_list 는 korean_output.csv 의 각 단과대별 과목 개수이다.
# check_rows_count.py를 통해 얻음
# 크롤링 할 때마다 rows_list_ko와 rows_list_en 변수 값 변경해줘야 됨
rows_list_ko = [0, 27, 314, 15, 27, 207, 124, 13, 77, 51, 130, 230, 96, 111, 95, 364, 61, 19, 128, 0, 245, 85, 134, 455, 29, 0, 152, 27, 819, 537, 4, 31, 95, 0, 42, 8, 0, 163, 0, 4, 0]
rows_list_en = [0, 27, 314, 15, 27, 207, 124, 13, 77, 51, 130, 230, 96, 111, 95, 364, 61, 19, 128, 0, 245, 85, 134, 455, 29, 0, 152, 27, 819, 537, 4, 31, 95, 0, 42, 42, 8, 0, 163, 0, 4, 0]

# korean csv
with open('../csv/korean/korean_output.csv', 'r', encoding='UTF-8-sig') as f1_ko :
    reader = csv.reader(f1_ko)
    header = next(reader)

    for i in range(len(rows_list_ko)) :
        results = []

        for j in range(rows_list_ko[i]) :
            results.append(next(reader))

        if rows_list_ko[i] == 0 :
            continue
        
        file_path = '../csv/korean/group/' + results[0][0] + '.csv'

        with open(file_path, 'w', encoding='utf-8-sig', newline='') as f2 :
            writer = csv.writer(f2)
            writer.writerow(header)
            for result in results :
                writer.writerow(result)

        f2.close()
f1_ko.close()


# english csv
with open('../csv/english/english_output.csv', 'r', encoding='UTF-8-sig') as f1_en:
    reader = csv.reader(f1_en)
    header = next(reader)

    for i in range(len(rows_list_en)):
        results = []

        for j in range(rows_list_en[i]):
            results.append(next(reader))

        if rows_list_en[i] == 0:
            continue

        if results[0][0] == 'Supplementary Term' :
            continue

        file_path = '../csv/english/group/' + results[0][0] + '.csv'

        with open(file_path, 'w', encoding='utf-8-sig', newline='') as f2:
            writer = csv.writer(f2)
            writer.writerow(header)
            for result in results:
                writer.writerow(result)

        f2.close()
f1_en.close()
