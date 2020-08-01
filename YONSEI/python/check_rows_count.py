from selenium import webdriver
import time

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')

url = 'https://portal.yonsei.ac.kr/main/index.jsp'
driver.get(url)

a_target = driver.find_element_by_css_selector('a#win_into_5_sugang')
a_target.click()

time.sleep(2)

driver.switch_to.window(driver.window_handles[-1])

# 학기 선택
semester_select = driver.find_element_by_css_selector('select#HG')
semester_options = semester_select.find_elements_by_css_selector('option')
semester_target = '2학기'

for semester_option in semester_options:
    if semester_option.text == semester_target:
        semester_option.click()
        
# 학부대학 선택
college_select = driver.find_element_by_css_selector('select#OCODE1')
college_options = college_select.find_elements_by_css_selector('option')

cnt = 0
li = []

for college_option in college_options:
    college_option.click()
    time.sleep(1)

    # 검색 script 실행
    search = "javascript:searchGb('search',1);"
    driver.execute_script(search)
    time.sleep(3)

    rows = driver.find_element_by_xpath("//*[@id='pager']/div/div/div[3]").text
    rows_range, rows = rows.split(" of ")
    rows_range_start, rows_range_finish = rows_range.split("-")

    rows = int(rows)

    li.append(rows)

    print(college_option.text, ":", rows, "과목")
    cnt += rows
    
    # print("Done")

print("count of all subject : ", cnt, "과목")
print(li)
time.sleep(1)

# webdriver 종료
driver.quit()

# result
"""
학부대학 : 0 과목
교양기초(2019학번~) : 27 과목
대학교양(2019학번~) : 314 과목
기초교육(2019학번~) : 15 과목
공통기초(10~18학번) : 27 과목
필수교양(10~18학번) : 207 과목
선택교양(10~18학번) : 124 과목
학부기초(~2009학번) : 13 과목
학부필수(~2009학번) : 77 과목
계열기초(~2009학번) : 51 과목
학부선택(~2009학번) : 130 과목
문과대학 : 230 과목
상경대학 : 96 과목
경영대학 : 111 과목
이과대학 : 95 과목
공과대학 : 364 과목
생명시스템대학 : 61 과목
신과대학 : 19 과목
사회과학대학 : 129 과목 -> 그 사이에 1과목 줄어서 128과목 됨
법과대학 : 0 과목
음악대학 : 245 과목
생활과학대학 : 85 과목
교육과학대학 : 134 과목
언더우드국제대학 : 455 과목
약학대학 : 29 과목
간호대학 : 0 과목
글로벌인재대학 : 152 과목
연계전공 : 27 과목
국제캠퍼스(2019학번~) : 819 과목
(~2018학번)국제캠퍼스 : 537 과목
ROTC : 4 과목
교직과정 : 31 과목
의과대학 : 95 과목
치과대학 : 0 과목
간호대학 : 42 과목
평생교육사과정 : 8 과목
계절학기 : 0 과목
Study Abroad Course : 163 과목
국내교환대학 : 0 과목
공통 : 4 과목
(~2007)국제교육부 : 0 과목
count of all subject :  4920 과목
"""