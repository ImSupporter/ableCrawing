import json
from lib2to3.pgen2 import driver
import bs4
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
from pyproj import Proj, transform

#----------------------------------------------------------------------------------------------------------------
def set_chrome_driver_mobile():
    mobile_emulation = {'deviceName':'iPhone X'}
    chrome_options = webdriver.ChromeOptions()

    #안보이게
    #chrome_options.add_argument('headless')
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
    # Projection 정의
    # 중부원점(Bessel): 서울 등 중부지역 EPSG:2097
proj_1 = Proj(init='epsg:2097')
    # WGS84 경위도: GPS가 사용하는 좌표계 EPSG:4326
proj_2 = Proj(init='epsg:4326')

# csv 파일 불러오기
total_gym = pd.read_csv(FILE_PATH,low_memory=False)
converted = transform(proj_1, proj_2, total_gym['좌표정보(x)'].values, total_gym['좌표정보(y)'].values)
total_gym['lon'] = converted[0]
total_gym['lat'] = converted[1]
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
        lon = gym['lon']
        lat = gym['lat']
        
        on_gym.append([gym_name, road_address, address, lat, lon])

print('전체 데이터 수 :',len(on_gym))
driver = set_chrome_driver_mobile()


for idx in range(70,100):
    if len(on_gym[idx][1]) == 0:
        search_query = on_gym[idx][2]
    else:
        search_query = on_gym[idx][1]
    driver.get('https://m.map.naver.com/#/search')
    sleep(2)
    searchBox = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="ct"]/div[1]/div[1]/form/div/div[2]/div/span[1]/input'))
    )
    searchBox.send_keys(search_query)
    searchBox.send_keys(Keys.ENTER)
    sleep(1)
    try:
        print(idx, search_query, on_gym[idx][0])
        addressBS = BeautifulSoup(driver.page_source, 'html.parser')
        placeList = addressBS.select('#ct > div.search_listview._content._ctAddress > ul > li')
        for i in placeList:
            category = i.select_one('div.item_info > a.a_item.a_item_distance._linkSiteview > div > em').text
            data_id = i['data-id']
            place_name = i['data-title']
            if category in ['헬스장', '스포츠시설', '체력단련,운동']:
                print(data_id, place_name, category)
    except:
        print("no result")
    finally:
        print()

