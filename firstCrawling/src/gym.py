import json
import requests
import ItemManager
from time import sleep
from selenium import webdriver   
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from pyproj import Proj, transform

#----------------------------------------------------------------------------------------------------------------
def set_chrome_driver_mobile():
    mobile_emulation = {'deviceName':'iPhone X'}
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('headless')
    #chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                              options=chrome_options)
    return driver

def send_api(y:float , x:float, page:int = 1, query:str = '헬스장'):
    API_URL = 'https://dapi.kakao.com/v2/local/search/keyword'
    headers = {'Authorization':'KakaoAK bbea4260b365b4a526a908b0d42b3b3d'}
    body = {
        'y': y,
        'x' : x,
        'radius' : '20000',
        'page' : page,
        'size' : 15,
        'query' : query,
        'sort' : 'distance'
    }

    response = requests.get(API_URL, data=body, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.content)
#----------------------------------------------------------------------------------------------------------------
#세팅
FILE_PATH = '/Users/parktaehyun/SmileHunter/Crawling/firstCrawling/fulldata_gym.csv'
    # Projection 정의
    # 중부원점(Bessel): 서울 등 중부지역 EPSG:2097
proj_1 = Proj(init='epsg:2097')
    # WGS84 경위도: GPS가 사용하는 좌표계 EPSG:4326
proj_2 = Proj(init='epsg:4326')

    
driver = set_chrome_driver_mobile()

# csv 파일 불러오기
total_gym = pd.read_csv(FILE_PATH,low_memory=False)

# csv 파일 전체 조회
on_gym=[]
print('전체 데이터 수 :',len(total_gym))
for i in range(len(total_gym)):
    gym = total_gym.loc[i]
    status_code = gym['영업상태구분코드']
    
    # 영업중인 장소(status code == 1)만 검색 후보에 추가
    if(status_code == 1):
        gym_name = gym['사업장명']
        road_address = gym['도로명전체주소']
        address = gym['소재지전체주소']
        on_gym.append([gym_name,road_address, address])
        
#검색(크롤링 시작)
for i in range(100):
    print(i,on_gym[i])
    driver.get('https://m.map.naver.com/#/search')
    sleep(0.5)
    #검색어 입력
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="ct"]/div[1]/div[1]/form/div/div[2]/div/span[1]/input'))
    )
    if type(on_gym[i][1]) is not float: #도로명로 검색
        search_box.send_keys(on_gym[i][0]+" "+on_gym[i][1].split(',')[0])
    else:   #도로명 주소가 없을 때 전체 주소로 검색
        search_box.send_keys(on_gym[i][0]+" "+on_gym[i][2].split(',')[0])
    driver.find_element(By.XPATH,'//*[@id="ct"]/div[1]/div[1]/form/div/div[2]/div/span[2]/button[2]').click()
    sleep(0.5)
    
    try:
        rank1_result = driver.find_element(By.XPATH,'//*[@id="ct"]/div[2]/ul/li/div[1]/a/div/strong').text
    except:
        print('결과 없음')
    sleep(1)


