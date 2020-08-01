from selenium import webdriver
import time

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')

url = 'https://portal.yonsei.ac.kr/main/indexe.jsp'
driver.get(url)

a_target = driver.find_element_by_css_selector('a#win_into_5_sugang')
a_target.click()

time.sleep(2)

driver.switch_to.window(driver.window_handles[-1])

# 학기 선택
semester_select = driver.find_element_by_css_selector('select#HG')
semester_options = semester_select.find_elements_by_css_selector('option')
semester_target = '2ND SEMESTER'

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

print("count of all subject : ", cnt, "과목")
print(li)
time.sleep(1)

# webdriver 종료
driver.quit()

"""
University College : 0 과목
Foundation Education(2019~) : 27 과목
General Education(2019~) : 314 과목
Basic Education(2019~) : 15 과목
General Education Basic(10~18) : 27 과목
General Education Requisite(10~18) : 207 과목
General Education Elective(10~18) : 124 과목
UC Basic(~2009) : 13 과목
UC Requisite(~2009) : 77 과목
General Area Basic(~2009) : 51 과목
UC Elective(~2009) : 130 과목
College of Liberal Arts : 230 과목
College of Commerce and Economics : 96 과목
College of Business : 111 과목
College of Science : 95 과목
College of Engineering : 364 과목
College of Life System : 61 과목
College of Theology : 19 과목
College of Social Science : 129 과목 -> 그 사이에 1과목 줄어서 128과목 됨
College of Law : 0 과목
College of Music : 245 과목
College of Human Ecology : 85 과목
College of Sciences in Education : 134 과목
Underwood International College : 455 과목
College of Pharmacy : 29 과목
College of Nursing : 0 과목
Global Leaders College : 152 과목
Joint Major : 27 과목
International Campus(2019~) : 819 과목
(~2018)International Campus : 537 과목
ROTC : 4 과목
Common Basic(11~19) : 31 과목
College of Medicine : 95 과목
College of Dentistry : 0 과목
College of Nursing : 42 과목
Supplementary Term : 42 과목 ! -> 이상 수정
Life-long Education Specialist Program : 8 과목
Supplementary Term : 0 과목
Study Abroad Course : 163 과목
Exchange Course : 0 과목
COMMON : 4 과목
(~2007)International Education and Exchange : 0 과목
count of all subject :  4962 과목
"""