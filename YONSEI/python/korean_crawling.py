from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv

# Setting
f = open('./xlsx/korean/korean_output.xlsx', 'w', encoding='utf-8-sig', newline='')
wr = csv.writer(f)

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

# 칼럼 카테고리 리스트는 따로 크롤링을 통하여 구하였음
column_categories = ['', None, None, '학년', '종별', '단위', '학정번호-분반(-실습)', '학점', '교과목명', '수강대상', None, None, None, '담당교수', '강의시간', '강의실', '유의사항', '국외교환학생가능']

# 영어 칼럼
# column_categories = ['', None, None, 'Year', 'Classification', 'Weight', 'Course Code-Sec.(-Lab)', 'Credit', 'Course Title', 'Target', None, None, None, 'Instructor', 'Time', 'Room', 'Ref', 'Exchange']

# None -> '' change
column_categories = ['' if v is None else v for v in column_categories]

# 1, 2 열에 학부대학, 소분류를 삽입하여 xlsx 작성
column_categories[0:0] = ["학부대학", "소분류"]
wr.writerow(column_categories)

# page 크롤링 시작
for college_option in college_options:
    college_option.click()
    time.sleep(1)

    # 학부대학 옵션은 과목이 없어서 시간 단축하기 위하여 생략
    if college_option.text == "학부대학":
        continue

    # 학과 선택(교양에 대해서는 소분류 선택)
    dept_select = driver.find_element_by_css_selector('select#S2')
    dept_options = dept_select.find_elements_by_css_selector('option')

    for dept_option in dept_options:
        # 학과 카테고리 별로 정리를 해야 하므로
        # 학과 옵션이 '전체'일 경우 pass -> 다음에 나오는 소분류만 선택
        if dept_option.text == '전체':
            continue

        # 학과 옵션 클릭
        dept_option.click()
        time.sleep(1)

        # 검색 script 실행
        search = "javascript:searchGb('search',1);"
        driver.execute_script(search)
        time.sleep(6)

        # 다음 페이지 선택 버튼을 미리 탐색
        # WebDriverWait, EC, By를 통해 구현해야 하는데, 너무 늦게 알아버려서 시간상 나중에 수정
        # 일단은 문제가 발생하지 않았음 -> 최적화 작업에서는 webdriver().until(EC.find_element())로 수정
        button = driver.find_element_by_xpath(
            "/html/body/div[5]/form[2]/table/tbody/tr[3]/td/div/div[2]/div/div[8]/div/div/div[2]/div")
        time.sleep(3)

        # rows : "1 - n of m" 형식의 string
        # " of " 기준으로 슬라이싱 하여 rows_range_start, rows_range_finish 구분
        # "-" 기준으로 슬라이싱 하여 전체 result rows 수를 구함
        rows = driver.find_element_by_xpath("//*[@id='pager']/div/div/div[3]").text
        rows_range, rows = rows.split(" of ")
        rows_range_start, rows_range_finish = rows_range.split("-")

        # 연산을 위해 string->int로 형변환
        rows = int(rows)
        rows_range_start = int(rows_range_start)
        rows_range_finish = int(rows_range_finish)
        time.sleep(1)

        # 조회된 rows 수가 0개라면 pass(continue를 해도 상관없다)
        if rows == 0:
            pass

        else:
            # cnt : 콘솔에 정보를 출력할 때, 과목 갯수 확인용
            cnt = 1

            # repeat : 연세대 과목 정보는 15개씩 보여지므로 다음 페이지로 넘어가는 버튼을 눌러야 하는데,
            # 이 때 다음 페이지를 클릭하는 횟수(= 크롤링 작업을 반복을 하는 횟수)
            # ex 1) 1 - 10 of 10 -> repeat = 1
            # ex 2) 1 - 15 of 15 -> repeat = 1
            # ex 3) 1 - 15 of 16 -> repeat = 2
            # ex 4) 1 - 15 of 43 -> repeat = 3
            # ex 5) 1 - 15 of 60 -> repeat = 4
            repeat = (rows - 1) // 15 + 1

            for i in range(repeat):
                time.sleep(1)
                # 반복 작업 할 때 마다 rows_range_start와 rows_range_finish 갱신
                rows = driver.find_element_by_xpath("//*[@id='pager']/div/div/div[3]").text
                print(college_option.text, dept_option.text, rows)

                rows_range, rows = rows.split(" of ")
                rows_range_start, rows_range_finish = rows_range.split("-")

                rows = int(rows)
                rows_range_start = int(rows_range_start)
                rows_range_finish = int(rows_range_finish)

                # 15개의 결과 -> 만약 rows < 15 인 경우라도, div의 개수는 15개로 고정됨(hidden 처리 안됨)
                result_rows = driver.find_elements_by_css_selector("div#contenttablejqxgrid > div")
                time.sleep(1)
                # print(len(result_rows)) -> 15개 rows

                # 첫 페이지뿐만 아니라 만약 마지막 페이지더라도 rows_range_finish - rows_range_start + 1 개의 결과값이 보여짐
                # rows >= 15인 경우, 첫 페이지는 15 - 1 + 1 = 15개의 결과값이 보여짐
                # 확신함!
                for j in range(rows_range_finish - rows_range_start + 1):
                    result_info = []

                    # 각 result의 column별 정보 수집
                    divs = result_rows[j].find_elements_by_xpath("div[@role='gridcell']")
                    # print(len(divs)) -> 18개 divs

                    for div in divs:
                        # 인덱스가 16인 부분은 유의사항에 해당됨.
                        # 유의사항 클릭 시 팝업이 뜨는데, 이때 해당되는 스크립트를 string으로 수집
                        # 팝업에는 해당 학과에 대한 유의사항이 뜨는데, 이는 사용자들이 직접 비교하면서 확인해야됨
                        # 때문에 해당 텍스트도 수집
                        if divs.index(div) == 16:
                            try:
                                element_a = div.find_element_by_css_selector("a")

                                href = element_a.get_attribute("href")
                                text = element_a.text

                                # 추후 xlsx 파일에서 슬라이싱 예정
                                result_info.append(href + ", " + text)

                            # href가 없는 경우(폐강, 기타 등) -> div.text만 append()
                            except:
                                print("\nError -> href : None")
                                result_info.append(div.text)

                        # 나머지 정보는 string으로 크롤링
                        else:
                            result_info.append(div.text)

                    # 콘솔에 logging -> 문제점 찾기 쉬움
                    print(cnt, result_info)

                    # 학부대학, 학과(소분류) 삽입하여 xlsx 작성
                    result_info[0:0] = [college_option.text, dept_option.text]
                    wr.writerow(result_info)

                    cnt += 1

                time.sleep(2)
                button.click()

        # 소분류별로 완료될 때마다 console에 "done" 출력
        print("done")

time.sleep(1)

# xlsx 작성 종료
f.close()

# webdriver 종료
driver.quit()
