import json
from lib2to3.pgen2 import driver
import this
import bs4
from numpy import place
import requests
import ItemManager
from time import sleep
from selenium import webdriver   
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

#----------------------------------------------------------------------------------------------------------------
def set_chrome_driver_mobile():
    mobile_emulation = {'deviceName':'iPhone X'}
    chrome_options = webdriver.ChromeOptions()

    #안보이게
    #chrome_options.add_argument('headless')
    #chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.57 Whale/3.14.133.23 Safari/537.36')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                              options=chrome_options)
    return driver

def send_api(y:float , x:float, page:int = 1, query:str = '헬스'):
    API_URL = 'https://dapi.kakao.com/v2/local/search/keyword'
    headers = {'Authorization':'KakaoAK bbea4260b365b4a526a908b0d42b3b3d'}
    body = {
        'y': y,
        'x' : x,
        'radius' : '500',
        'page' : page,
        'size' : 3,
        'query' : query,
        'sort' : 'accuracy',
        'category_group_code' : 'CT1'
    }

    response = requests.get(API_URL, data=body, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.content)
#----------------------------------------------------------------------------------------------------------------
#세팅
FILE_PATH = 'firstCrawling/fulldata_gym.csv'

# csv 파일 불러오기
total_gym = pd.read_csv(FILE_PATH,low_memory=False)
# csv 파일 전체 조회
on_gym=[]
for i in range(len(total_gym)):
    gym = total_gym.loc[i]
    status_code = gym['영업상태구분코드']
    
    # 영업중인 장소(status code == 1)만 검색 후보에 추가
    if(status_code == 1):
        gym_name = gym['사업장명']
        road_address = str(gym['도로명전체주소']).split(',')[0]
        address = str(gym['소재지전체주소']).split(',')[0]
        
        on_gym.append([gym_name, road_address, address])

print('전체 데이터 수 :',len(on_gym))
driver = set_chrome_driver_mobile()
driver.implicitly_wait(3)

# 크롤링 시작 -------------------------------------------------------------------
startIdx = 2955
for idx in range(startIdx, len(on_gym)):
    if len(on_gym[idx][1]) < 5:
        search_query = on_gym[idx][2]
    else:
        search_query = on_gym[idx][1]
    #검색창 열기
    driver.get('https://m.map.naver.com/#/search')
    searchBox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="ct"]/div[1]/div[1]/form/div/div[2]/div/span[1]/input'))
    )
    searchBox.send_keys(search_query)
    searchBox.send_keys(Keys.ENTER)
    
    #검색 결과
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ct"]/div[2]/ul'))
        )
    except:
        continue
    sleep(2)
    print(idx, search_query, on_gym[idx][0])
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    sleep(3)
    addressBS = BeautifulSoup(driver.page_source, 'html.parser')
    placeList = addressBS.select('#ct > div.search_listview._content._ctAddress > ul > li')
    for i in placeList:
        # 해당 주소의 장소중 카테고리가 헬스장, 스포츠 시설, 체력단련,운동인 장소만 가져오기
        category = i.select_one('div.item_info > a.a_item.a_item_distance._linkSiteview > div > em').text
        if category in ['헬스장', '스포츠시설', '체력단련,운동', '체육관', '실내체육관']:
            #데이터 추출
            data_id = i['data-id']
            place_name = i['data-title']
            place_tel = i['data-tel']
            longitude = i['data-longitude']
            latitude = i['data-latitude']
            naver_road_address = i.select_one('div.item_info > div.item_info_inn > div > a').text[5:].strip()
            try:
                thumnail = i.select_one('div.item_info > a.item_thumb._itemThumb > img')['src']
            except:
                thumnail = None
            # 데이터 미리 보기
            print(data_id, place_name, naver_road_address)
            print(place_tel, latitude, longitude, thumnail)
            
            # 데이터 베이스에 크롤링한 내용 넣기
            if ItemManager.place_search(data_id) is None:
                ItemManager.place_insert(data_id,'GYM', place_name, naver_road_address,place_tel, latitude, longitude, thumnail)
            else:
                print('existed')
    print()

