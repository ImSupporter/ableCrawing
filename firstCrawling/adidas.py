import ItemManager
from multiprocessing.connection import wait
from this import d
from time import sleep
from webbrowser import Chrome
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
#----------------------------------------------------------------------------------------------------------------
baseUrl = "https://www.adidas.co.kr"
path_top = [
    #'/men-hoodies%7Csweatshirts',
    #'/men-football-jerseys',
    #"/men-jackets",
    #'/men-t_shirts',
    '/men-tracksuits',
    
    '/women-jackets',
    '/women-hoodies%7Csweatshirts',
    '/women-t_shirts',
    '/women-tracksuits',
    '/women-sports_bras'    
]
path_bottom = [
    '/men-pants',
    '/men-shorts',
    
    '/women-pants',
    '/women-tights',
    '/women-shorts',
    '/women-skirts',
    '/women-dresses'
]
path_shoes = [
    '/men-shoes',
    '/women-shoes'
]
path_headwear=['/men-headwear', '/women-headwear']

total_path = {'BOTTOM':path_bottom, 'SHOES':path_shoes, 'HEADWEAR':path_headwear}
#'TOP':path_top,
#----------------------------------------------------------------------------------------------------------------
driver = set_chrome_driver()
driver.get(baseUrl)
driver.find_element(By.XPATH,'//*[@id="modal-root"]/div/div/div/div[2]/div/div[2]/button[1]').click() # 쿠키정책동의



for sub, sub_urls in total_path.items():
    print(sub)
    sub_category = sub
    for u in sub_urls:
        sub_url = baseUrl + u
        driver.get(sub_url)
        sleep(1)
        print("시작 :", u)
        itemLink = []
        num = 0
        #itemLink에 모든 item link 넣기
        for page in range(999):                                                        
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div[2]/div[1]'))) # item grid
            bs = BeautifulSoup(driver.page_source, 'html.parser') # page 파싱
            for item in bs.select(".plp-grid___hCUwO .glass-product-card-container>div>a"): #아이템 url만 가져오기
                link = item.attrs['href']
                itemLink.append(link)
                num+=1
            bs = None
            try:# 다음 버튼이 있으면 다음 페이지로
                driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/a/span').click()
                sleep(1)
            except:# 없으면 해당 카테고리는 끝
                print("끝")  
                break
            
        num = 0    
        for i in itemLink:
            print(num,':',i)
            num+=1
            
        num = 0    
        for url in itemLink: #링크에 있는 아이템 정보를 가져와 DB에 저장                               
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#navigation-target-specifications > div.specifications__table___3C17U > div > div > div:nth-child(1) > div:nth-child(2) > div')))
            except:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#navigation-target-specifications > div > div.specifications__table___3C17U > div > div > div:nth-child(1) > div:nth-child(2) > div')))
            item_soup = BeautifulSoup(driver.page_source, 'html.parser')
            item_name = item_soup.select_one('#app > div > div:nth-child(1) > div > div > div > div.content-wrapper___3AhOy > div.sidebar-wrapper___26z7B > div.sidebar___2C-EP > div > h1 > span').get_text()
            price  = item_soup.select_one('#app > div > div:nth-child(1) > div > div > div > div.content-wrapper___3AhOy > div.sidebar-wrapper___26z7B > div.sidebar___2C-EP > div > div.product-price___gJhOl.gl-vspace > div > div > div > div').get_text()
            price = int(price[:-2].replace(",",""))
            try:
                item_code = item_soup.select_one('#navigation-target-specifications > div.specifications__table___3C17U > div > div > div:nth-child(1) > div:nth-child(2) > div').get_text()
            except:
                item_code = item_soup.select_one('#navigation-target-specifications > div > div.specifications__table___3C17U > div > div > div:nth-child(1) > div:nth-child(2) > div').get_text()
            print(num,":",item_name, price,item_code)
            
            
            if ItemManager.search(item_code) is None: # Database에 저장하기(해당 item code가 없을 때)
                ItemManager.insert('adidas', item_name, item_code, 'CLOTHES',sub_category, price, url)
            else:
                print('이미있음')
            num+=1
#종료
driver.close()



