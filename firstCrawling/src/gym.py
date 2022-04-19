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

#----------------------------------------------------------------------------------------------------------------
def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('headless')
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
num = 1
page = 1
for i in range(99999999):
    response = send_api(y = 37.514322572335935, x = 127.06283102249932,page=page)
    meta = response['meta']
    if page == 1:
        print('전체 결과 수',':',meta['total_count'])
    document = response['documents']
    for p in document:
        print(num, ':', p['place_name'],':', p['road_address_name'])
        num+=1
    print("---------------------------------------------------")
    page+=1
    if meta['is_end'] is True:
        break