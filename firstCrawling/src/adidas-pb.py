from urllib.parse import unquote
import ItemManager
from time import sleep
from selenium import webdriver   
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from model.item import addBrandByItemCode

#----------------------------------------------------------------------------------------------------------------
def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                              options=chrome_options)
    return driver
#----------------------------------------------------------------------------------------------------------------
baseUrl = "https://www.adidas.co.kr"
pb_path = {
    #"/originals" : 2,   
    "/y_3" : 3,         #3
    "/sportswear" : 4,  #4
    "/terrex" : 5 ,      #5
    "/adidas_by_stella_mccartney" : 6 #6
}

driver = set_chrome_driver()
driver.implicitly_wait(5)
driver.get(baseUrl)
driver.find_element(By.XPATH,'//*[@id="modal-root"]/div/div/div/div[2]/div/div[2]/button[1]').click() # 쿠키정책동의


item_links = []
for path, brand_id in pb_path.items():       #   pb 브랜드 루프
    #pb url
    url = baseUrl + path
    driver.get(url)
    
    for i in range(999):    # 페이지 목록 루프
        grid = driver.find_elements(By.CLASS_NAME, 'grid-item')
        print(len(grid))
        for idx, g in enumerate(grid):
            item_url = g.find_element(By.CSS_SELECTOR, 'div > div > div > div > div > div > div > a').get_attribute('href')
            item_url = unquote(item_url)
            print(idx, item_url)
            item_links.append(item_url)
        
        try: #다음 버튼 누르기
            driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/a').click()
            sleep(2)
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME,'glass-product-card__assets-link'))
            )
        except:
            break;
    
    #브랜드(id) 추가
    for idx, link in enumerate(item_links):
        item_code = link.split('/')[-1].replace('.html','')
        addBrandByItemCode(item_code,brand_id)
    item_links.clear()