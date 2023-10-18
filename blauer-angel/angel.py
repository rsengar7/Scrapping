import time, sys, os
import wget
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
from csv import writer

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.blauer-engel.de/de/marken")

time.sleep(2)

'//*[@id="edit-submit-pdf"]'
'//*[@id="edit-submit-pdf"]'

'//*[@id="edit-submit-xlsx"]'

Names = []
Links = []
for alphabet in range(2, 29):
    for tag in range(1, 150):
        '//*[@id="block-be-content"]/article/div[3]/div/div/div/div[{}]/ul/li[{}]/a'
        try:
            button = driver.find_element(by=By.XPATH, value='//*[@id="block-be-content"]/article/div[3]/div/div/div/div[{}]/ul/li[{}]/a'.format(alphabet, tag))
            print(button.text.split('(')[0].strip())
            print(button.get_attribute('href'))
            print()
            Names.append(button.text.split('(')[0].strip())
            Links.append(button.get_attribute('href'))
        except Exception as e:
            print("Error -->",e)
            pass

dict1 = {
    "Names": Names,
    "Links": Links
}

df = pd.DataFrame(dict1)

df.to_csv('blauer-engel.csv')

# Links = ['https://www.blauer-engel.de/de/marken/awo-seniorenzentrum', 'https://www.blauer-engel.de/de/marken/avia']

# for index, link in enumerate(Links):
#     driver.get(link)

#     button = driver.find_element(by=By.XPATH, value='//*[@id="edit-submit-pdf"]')
#     # print(button.get_attribute('href'))
#     # print()
#     driver.execute_script("arguments[0].click();", button)
#     if index+1 == len(Links):
#         time.sleep(30)
    
