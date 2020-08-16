from selenium import webdriver
import csv
import time

def major_name_nomalization(name):
    name = name.split()
    result = ''

    for n in name :
        result = result + n + " "

    temp_result = ''
    temp_cnt = 3
    while True :
        if result[-temp_cnt] == '(':
            break
        temp_result += result[-temp_cnt]
        temp_cnt += 1

    result = temp_result[::-1]
    return result

# Setting
f = open('../csv/output.csv', 'w', encoding='utf-8-sig', newline='')
wr = csv.writer(f)

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')

url = 'https://wis.hufs.ac.kr/src08/jsp/lecture/LECTURE2020L.jsp'
driver.get(url)

time.sleep(2)

cnt = 0

header = ["전공", "영역", "학수번호", "과목명", "교수명", "이수구분", "학년", "학점", "강의시간/강의실"]
wr.writerow(header)

# 글로벌캠퍼스 선택
driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[3]/td/label[2]').click()
time.sleep(3)

# 전공 선택
driver.find_element_by_xpath("/html/body/div/form/div[1]/table/tbody/tr[4]/th").click()
time.sleep(3)

major_options = driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[4]/td/div/select').find_elements_by_css_selector('option')
time.sleep(1)

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

        # 중분류(전공/부전공 or 실용외국어/교양)
        result_list.append("Major/Minor")

        # 소분류(학과)
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

        print(result_list)
        wr.writerow(result_list)

    cnt += 1
    time.sleep(2)

# 영어교양 선택
cnt = 0

driver.find_element_by_xpath("/html/body/div/form/div[1]/table/tbody/tr[5]/th").click()
time.sleep(3)

major_options = driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[5]/td/div/select').find_elements_by_css_selector('option')
time.sleep(1)

for option in range(len(major_options)) :
    major_options = driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[5]/td/div/select').find_elements_by_css_selector('option')
    time.sleep(2)

    temp_name = major_options[cnt].text
    major_name = temp_name

    major_options[cnt].click()
    time.sleep(1)
    search = 'javascript:time_submit();'
    driver.execute_script(search)

    rows = driver.find_elements_by_css_selector("#premier1 > div > table > tbody > tr")

    for i in range(1, len(rows)):
        result_list = []

        # 중분류(전공/부전공 or 실용외국어/교양)
        result_list.append("Practical foreign language/Liberal arts")

        # 소분류(학과)
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

        print(result_list)
        wr.writerow(result_list)

    cnt += 1
    time.sleep(2)

f.close()
driver.quit()