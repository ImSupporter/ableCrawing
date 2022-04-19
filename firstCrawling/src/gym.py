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
#----------------------------------------------------------------------------------------------------------------
driver = set_chrome_driver()
driver.get('https://map.kakao.com/')

sleep(2)
driver.close()