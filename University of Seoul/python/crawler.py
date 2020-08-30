from selenium import webdriver
import csv
import time

# Setting
f = open('../xlsx/output.csv', 'w', encoding='utf-8-sig', newline='')
wr = csv.writer(f)

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')

url = 'https://global.uos.ac.kr/iice/study/prEnglish.do?epTicket=LOG'
driver.get(url)

time.sleep(3)

table = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[2]/div/table")
time.sleep(1)

rows = table.find_element_by_css_selector('tbody').find_elements_by_css_selector('tr')


for row in rows :
    result = []

    tds = row.find_elements_by_css_selector('td')

    for td in tds :
        result.append(td.text)

    wr.writerow(result)

f.close()
driver.quit()