# from tkinter.tix import Select

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# 설치된거 쓰는 버전
driver = webdriver.Chrome()

def init_url():
    # 시작 페이지 URL
    url = 'https://dart.fss.or.kr/dsae001/main.do#none'
    driver.get(url)
    time.sleep(3)  # 페이지 로딩 대기

def input_num(num):
    # 사업자등록번호 num parsing
    num_li = num.split('-')
    num_1 = num_li[0]
    num_2 = num_li[1]
    num_3 = num_li[2]
    data = []
    try:
        select_element = driver.find_element(By.CLASS_NAME, 'w10')

        # 셀렉트박스 선택
        select_box = Select(select_element)
        select_box.select_by_visible_text('사업자등록번호')
        time.sleep(1)

        # 사업자등록번호 입력
        input_element = driver.find_element(By.ID, 'bsnRgsNo_1')
        input_element.clear()
        input_element.send_keys(num_1)
        input_element = driver.find_element(By.ID, 'bsnRgsNo_2')
        input_element.clear()
        input_element.send_keys(num_2)
        input_element = driver.find_element(By.ID, 'bsnRgsNo_3')
        input_element.clear()
        input_element.send_keys(num_3)
        input_element.send_keys(Keys.RETURN)
        time.sleep(1)

        # 검색 결과 클릭 (첫 행 고정 선택)
        xpath = '//*[@id="corpTabel"]/tbody/tr/td[1]/span/a'
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        print(first_result.text)
        first_result.click()
        time.sleep(1)

        # 상세 검색 결과 수집
        table_element = driver.find_elements(By.XPATH, '//*[@id="corpDetailTabel"]')
        print(table_element[0].tag_name)
        rows = table_element[0].find_elements(By.XPATH, './/tr')

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            cell_texts = [cell.text.strip() for cell in cells]
            if cell_texts:
                data.append(cell_texts)
        # print(data)

    except Exception as ex:
        print(ex)

    return data

# 전체 게시글을 담을 리스트
all_rows = []
tmp_com = ['120-81-08227', '124-81-00998']
init_url()

# Read list
for i in range(len(tmp_com)):
    tmp = input_num(tmp_com[i])
    print(tmp)
    all_rows.append(tmp)

df = pd.DataFrame(all_rows)
print(df)

df.to_csv('./tmp.csv', index=False)