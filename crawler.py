import pandas as pd    # 판다스 : 데이터분석 라이브러리
import numpy as np     # 넘파이 : 숫자, 행렬 데이터 라이브러리

from bs4 import BeautifulSoup     # html 데이터 전처리
from selenium import webdriver    # 웹 브라우저 자동화 (click이 지역별 데이터 크롤링 전 단계에서 필요함)
import time                       # 시간 지연(시간을 너무 빠르게하면 튕기거나 오류 발생)
from tqdm import tqdm_notebook    # 진행상황 표시
from selenium.webdriver.chrome.service import Service # service = Service(r"C:\Users\user\Desktop\IDE\vscode\112\chromedriver.exe") 이부분 오류 방지
from selenium.webdriver.common.by import By           # find_element함수를 사용하기 위해서
from selenium.common.exceptions import NoSuchElementException# driver.find_element(By.XPATH, element3).click()부분 오류 방지

address_list = []        # 주소 O
text_list = []           # 대 # 대는 건물 매매의 경우 생략 O
deal_list = []           # 거래 방식 O
won_list =  []           # 가격 O
kind_list = []           # 토지 # 토지 생략? O
area_list = []           # 면적 O

generation_list = []     # 세대수 
apprpval_date_list = []  # 사용승인일
area_ratio_list = []     # 용적율(값 없을 수 있음)
con_com_list = []        # 건설사
heating_list = []        # 난방
management_list = []     # 관리사무소
floors_list = []         # 저/최고층
parking_spaces = []      # 총주차대수
coverage_ratio_list = [] # 건폐율

# 크롬 웹브라우저 실행
service = Service(r"C:\Users\user\Desktop\IDE\vscode\112\chromedriver.exe") #이 부분에 크롬 브라우저 위치
driver = webdriver.Chrome(service=service) 

# 사이트 주소
driver.get("https://new.land.naver.com/offices?ms=36.3615444,127.3784552,14&a=SG:SMS:GJCG:APTHGJ:GM:TJ&e=RETAIL")
time.sleep(2) #시간을 짧게하면 튕기는 오류 발생

# 아파트 클릭
driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/a[1]/span/em[1]").click() #아파트 항목에 해당하는 XPATH주소를 가져오고 해당 위치를 클릭해서 선택 
time.sleep(1) 

driver.find_element(By.CSS_SELECTOR, ".filter_btn_select").click() 
driver.find_element(By.XPATH, "/html/body/div[2]/div/section/div[1]/div/div[1]/div/div[1]/div/ul/li[2]/label").click() 
driver.find_element(By.CSS_SELECTOR, ".btn_close").click() 

# 상가, 사무실, 공장/창고, 지식산업센터, 건물 클릭으로 해제 없어짐 (토지에서 확인) 
# 필요 자료 확인 후 적용 

# 시 클릭
driver.find_element(By.XPATH, "/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/a/span[1]").click()
time.sleep(0.5)

# 서울시 클릭
driver.find_element(By.XPATH, "/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[2]/ul/li[1]/label").click()
time.sleep(0.5)

# 구 목록 가져오기
address1 = driver.find_element(By.CSS_SELECTOR, ".area_list--district").text.split() 

# 구 클릭
for i1 in range(1, len(address1)+1): #함수 작동방식 파악
    time.sleep(0.5) 
    #element1 = "/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/div/div[2]/ul/li[{}]/label".format(i1)
    element1 = "/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[2]/ul/li[{}]/label".format(i1) 
    driver.find_element(By.XPATH, element1).click() #위에서 정의내린 driver 확인
    time.sleep(0.5)
    
    # 동 목록 가져오기
    address2 = driver.find_element(By.CSS_SELECTOR, ".area_list--district").text.split()

    # 동 클릭
    for i2 in range(1, len(address2)+1):
        
        if i2 >= 2: #동 목록 켜기
            driver.find_element(By.XPATH, "/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/a/span[3]").click()
            time.sleep(0.5)
            driver.find_element(By.XPATH, "/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/a/span[3]").click()
            time.sleep(0.5)
            
        #element2 = "/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/div/div[2]/ul/li[1]/label".format(i2)
        element2 = "/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[2]/ul/li[{}]/label".format(i2) 
        driver.find_element(By.XPATH, element2).click()
        time.sleep(0.5)
        # 단지 부분에서 오류 발생
        # 단지 목록 가져오기
        address3 = driver.find_element(By.CSS_SELECTOR, ".area_list--complex").text.split()
        # /html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[2]/ul/li[2]/label/text()
        #/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[3]/ul/li[1]/a
        # 단지 클릭 /html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[2]/ul/li[1]
        for i3 in range(1, len(address3)):
            #element2 = "/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/div/div[2]/ul/li[{}]/label".format(i2)
            element3 = "/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[3]/ul/li[{}]/a".format(i3)
            try:
                driver.find_element(By.XPATH, element3).click()
            except NoSuchElementException: # .area_list--complex안에 있는 li개수가 실제 단지의 개수를 초과하여 단지를 끝까지 크롤링하면 반복문을 종료하고 다음 동을 크롤링하도록했습니다.                     
                driver.find_element(By.XPATH, "/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/a/span[3]").click() # 동 클릭을 하는 이유는 이전에 펼쳐져 있는 단지창을 끄기 위해서입니다.
                break
            time.sleep(1)
            # 단지 클릭/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[3]/ul/li[{}]/label
    
            # 크롤링
            item = driver.find_element(By.CSS_SELECTOR, ".item_list.item_list--article").text #list 부분에 들어있는 모든 텍스트 
            
            item_text = item.split('\n')

            ok_num = list(filter(lambda x: ('spec' in item_text[x]), range(len(item_text)))) #토지 면적에서 건물 평수 수정

            # 대 
            for i in ok_num:
                text_list.append(item_text[i-2]) # 대는 건물의 경우 생략후 리스트 적용

            # 거래 방식
            for i in ok_num:
                deal_list.append(item_text[i-1][0:2])

            # 가격
            for i in ok_num:

                price = item_text[i-1][2:]
                # 가격에 억 이하 단위가 없을 시 0000 삽입
                if price[-1] =='억':
                    price = price + '0000'

                # (억 , 띄워쓰기) 제거
                won = ''.join( x for x in price if x not in '억, ')
                # 원 단위로 변환
                won += '0000'
                won_list.append(int(won))

            # 토지
            for i in ok_num:
                kind_list.append(item_text[i][0:2])

            # 면적
            for i in ok_num:
                area = item_text[i][2:-2]
                area_list.append(int(area))
            
            # 주소 저장
            address = address1[i1-1], address2[i2-1]
            for i in ok_num:
                address_list.append(address)

            print(address1[i1-1], address2[i2-1], len(address_list), len(text_list), len(deal_list), len(won_list), len(kind_list), len(area_list)) #진행상황 표시
            
            driver.find_element(By.XPATH, "/html/body/div[2]/div/section/div[2]/div[2]/div/button").click() # X버튼####
            # 시 클릭
            driver.find_element(By.XPATH, "/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/a/span[1]").click()
            time.sleep(0.5)

            # 서울시 클릭
            driver.find_element(By.XPATH, "/html/body/div[2]/div/section/div[2]/div/div[1]/div/div/div/div[2]/ul/li[1]/label").click()
            time.sleep(0.5)

            driver.find_element(By.XPATH, element1).click() # 구 클릭
            time.sleep(0.5)
            
            driver.find_element(By.XPATH, element2).click() # 동 클릭            
            time.sleep(0.5)
        
    
    time.sleep(0.5)
    driver.find_element(By.XPATH, "/html/body/div[2]/div/section/div[2]/div[2]/div[1]/div/div/a/span[2]").click() # 구 클릭
        
df = pd.DataFrame({'주소':address_list, '구분':text_list, '거래방식':deal_list, '가격':won_list, '대지형태':kind_list, '면적':area_list})
df

df.info()

df.to_excel('crawler_naver 부동산매매.xlsx')