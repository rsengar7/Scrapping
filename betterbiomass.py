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

driver.get("https://nen.bettywebblocks.com/view-nta8080")

time.sleep(10)

li = []
li1 = []
li2 = []
li3 = []
li4 = []
li5 = []
li6 = []
li7 = []
li8 = []
li9 = []

'//*[@id="NTA8080"]/tbody/tr[1]'
'//*[@id="NTA8080"]/tbody/tr[2]'
'//*[@id="NTA8080"]/tbody/tr[188]'

'//*[@id="NTA8080"]/tbody/tr[1]/td[1]'

for i in range(1, 189):

    company_name = driver.find_element(by=By.XPATH, value='//*[@id="NTA8080"]/tbody/tr[{}]/td[1]'.format(i))
    company_text = company_name.text
    print(company_text)
    li.append(company_text)

    company_name = driver.find_element(by=By.XPATH, value='//*[@id="NTA8080"]/tbody/tr[{}]/td[2]'.format(i))
    company_text = company_name.text
    print(company_text)
    li1.append(company_text)

    company_name = driver.find_element(by=By.XPATH, value='//*[@id="NTA8080"]/tbody/tr[{}]/td[3]'.format(i))
    company_text = company_name.text
    print(company_text)
    li2.append(company_text)

    company_name = driver.find_element(by=By.XPATH, value='//*[@id="NTA8080"]/tbody/tr[{}]/td[4]'.format(i))
    company_text = company_name.text
    print(company_text)
    li3.append(company_text)

    company_name = driver.find_element(by=By.XPATH, value='//*[@id="NTA8080"]/tbody/tr[{}]/td[5]'.format(i))
    company_text = company_name.text
    print(company_text)
    li4.append(company_text)

    company_name = driver.find_element(by=By.XPATH, value='//*[@id="NTA8080"]/tbody/tr[{}]/td[6]'.format(i))
    company_text = company_name.text
    print(company_text)
    li5.append(company_text)

    company_name = driver.find_element(by=By.XPATH, value='//*[@id="NTA8080"]/tbody/tr[{}]/td[7]'.format(i))
    company_text = company_name.text
    print(company_text)
    li6.append(company_text)

    company_name = driver.find_element(by=By.XPATH, value='//*[@id="NTA8080"]/tbody/tr[{}]/td[8]'.format(i))
    company_text = company_name.text
    print(company_text)
    li7.append(company_text)

    company_name = driver.find_element(by=By.XPATH, value='//*[@id="NTA8080"]/tbody/tr[{}]/td[9]'.format(i))
    company_text = company_name.text
    print(company_text)
    li8.append(company_text)

    company_name = driver.find_element(by=By.XPATH, value='//*[@id="NTA8080"]/tbody/tr[{}]/td[10]'.format(i))
    company_text = company_name.text
    print(company_text)
    li9.append(company_text)

    
    # break

dict1 = {
    "Organization": li,
    "Country": li1,
    "Scope of Certificates": li2,
    "Products": li3,
    "Certifying Body": li4,
    "Version": li5,
    "Legal compliance": li6,
    "Status": li7,
    "1st Registry": li8,
    "Expiry": li9
}

df = pd.DataFrame(dict1)
df.to_csv('BetterBiomas.csv')