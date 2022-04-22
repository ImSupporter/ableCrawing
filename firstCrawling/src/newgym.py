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
        'sort' : 'distance',
        'size' : 1
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
        road_address = gym['도로명전체주소']
        address = gym['소재지전체주소']
        lon = gym['lon']
        lat = gym['lat']
        
        on_gym.append([gym_name,road_address, address, lat, lon])

print('전체 데이터 수 :',len(on_gym))
kakao_result = send_api(on_gym[11][3],on_gym[11][4],query=on_gym[11][0])
print(on_gym[11])
print(kakao_result)
# for i in range(90,100):
    
'''     
#검색(크롤링 시작)
for i in range(95,100):
    print(i,on_gym[i])
    driver.get('https://m.map.naver.com/#/search')
    sleep(2)
    #검색어 입력
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="ct"]/div[1]/div[1]/form/div/div[2]/div/span[1]/input'))
    )
    if type(on_gym[i][1]) is not float: #도로명으로 검색
        search_box.send_keys(on_gym[i][1].split(',')[0]+" "+on_gym[i][0])
    else:   #도로명 주소가 없을 때 전체 주소로 검색
        search_box.send_keys(on_gym[i][2].split(',')[0]+" "+on_gym[i][0])
    search_box.send_keys(Keys.ENTER)
    
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="ct"]/div[2]/ul/li/div[1]/a/div/strong'))
        )
        rank1_name = driver.find_element(By.XPATH,'//*[@id="ct"]/div[2]/ul/li[1]').get_attribute('data-title')
        rank1_road_address  = driver.find_element(By.XPATH, '//*[@id="ct"]/div[2]/ul/li[1]/div[1]/div[1]/div/a').text
        rank1_road_address = rank1_road_address[5:]
        rank1_number = driver.find_element(By.XPATH,'//*[@id="ct"]/div[2]/ul/li[1]').get_attribute('data-tel')
        rank1_thumnail = driver.find_element(By.XPATH,'//*[@id="ct"]/div[2]/ul/li[1]/div[1]/a[1]/img').get_attribute('src')
        rank1_nid = driver.find_element(By.XPATH,'//*[@id="ct"]/div[2]/ul/li[1]').get_attribute('data-id')
        rank1_lat = driver.find_element(By.XPATH,'//*[@id="ct"]/div[2]/ul/li[1]').get_attribute('data-latitude')
        rank1_lon = driver.find_element(By.XPATH,'//*[@id="ct"]/div[2]/ul/li[1]').get_attribute('data-longitude')
        print(rank1_name,rank1_road_address,rank1_number, rank1_thumnail, rank1_nid, rank1_lat,rank1_lon,sep="\n")
    except:
        print('결과 없음')
'''


