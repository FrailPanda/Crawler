from selenium import webdriver
import csv
import time

# Setting
f = open('../csv/output.csv', 'w', encoding='utf-8-sig', newline='')
wr = csv.writer(f)

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')

url = 'https://wis.hufs.ac.kr/src08/jsp/lecture/LECTURE2020L.jsp'
driver.get(url)

time.sleep(2)

# 전공 선택
major_options = driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[4]/td/div/select').find_elements_by_css_selector('option')
time.sleep(1)

cnt = 0

header = ["전공", "학수번호", "과목명", "교수명", "이수구분", "학년", "학점", "강의시간/강의실"]
wr.writerow(header)

def major_name_nomalization(name):
    name = name.split()
    result = ''

    del name[0]
    del name[0]

    for n in name :
        result = result + n + " "

    result = result.split("(")
    result = result[1][:-2]
    return result

for option in range(len(major_options)) :
    major_options = driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[4]/td/div/select').find_elements_by_css_selector('option')
    time.sleep(2)

    temp_name = major_options[cnt].text
    major_name = major_name_nomalization(temp_name)

    major_options[cnt].click()
    time.sleep(1)
    search = 'javascript:time_submit();'
    driver.execute_script(search)

    rows = driver.find_elements_by_css_selector("#premier1 > div > table > tbody > tr")

    for i in range(1, len(rows)):
        result_list = []

        # 전공
        result_list.append(major_name)

        row = rows[i]
        td = row.find_elements_by_css_selector("td")

        # 학수번호
        result_list.append(td[3].text)

        # 과목명
        result_list.append(td[4].text)

        # 교수명
        result_list.append(td[11].text)

        # 이수구분
        result_list.append(td[1].text)

        # 학년
        result_list.append(td[2].text)

        # 학점
        result_list.append(td[12].text)

        # 강의시간/강의실
        result_list.append(td[14].text)

        wr.writerow(result_list)


    cnt += 1
    time.sleep(2)

f.close()
driver.quit()