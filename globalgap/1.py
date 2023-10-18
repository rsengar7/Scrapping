import time, sys, os, re
import wget
import openpyxl
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
from csv import writer

# from func import extraction

chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu') 
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

'//*[@id="doc-table"]/tbody/tr[1]'
'//*[@id="doc-table"]/tbody/tr[2]'
'//*[@id="doc-table"]/tbody/tr[1343]'

'//*[@id="doc-table"]/tbody/tr[1]/td[1]/div/div[1]/a'
'//*[@id="doc-table"]/tbody/tr[2]/td[1]/div/div[1]/a'

driver.get("https://www.globalgap.org/uk_en/documents/")
time.sleep(30)

# uridiction = driver.find_element(by=By.XPATH, value='//*[@id="doc-table"]/tbody/tr[1]/td[1]/div/div[1]/a')
# # uridiction.click()
# print(uridiction.text)
# print(uridiction.get_attribute('href'))

# time.sleep(20)

for i in range(1, 1344):
    uridiction = driver.find_element(by=By.XPATH, value='//*[@id="doc-table"]/tbody/tr[{}]/td[1]/div/div[1]/a'.format(i))
    url = uridiction.get_attribute('href')
    print(i,"--",uridiction.text)
    # print(uridiction.text)

    wget.download(url, "Pdf/"+str(url).split("/")[-1])
    # time.sleep(5)