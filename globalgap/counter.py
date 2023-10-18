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

from func import extraction

chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu') 
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

df = pd.read_csv("Secretary of State's Government Records.csv")
url = df['Company Url'].apply(lambda x: x.split("/")[-1]).values.tolist()

df1 = pd.read_csv('row_data.csv')
# df1 = pd.read_csv('exist.csv', on_bad_lines='skip')
add = df1['URL'].apply(lambda x: x.split("/")[-1]).values.tolist()

# print(df1.head())
# sys.exit()
df2 = pd.read_csv("tried_number.csv", dtype={"Number":"string"})
tried = df2['Number'].astype(str).values.tolist()

url_data = url+add+tried

from itertools import permutations

char = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

comb = permutations(digits, 6)

company_name = []
company_url = []
company_number = []
status = []
incorporation_date = []
disoolution = []
company_type = []
Juridiction = []
business_classification_text = []
PreviousName = []
AgentName = []
AgentAddress = []
attribute_list = []
registry_page = []


f = open("row_data.csv", 'a')
f1 = open("tried_number.csv", 'a')
counter = 0
row_entry = ""
for index, num in enumerate(comb): 
    num = list(num)
    num.insert(3, "-")
    numbers = "".join([i for i in num])
    # print(numbers)
    # sys.exit()

    base_url = "https://opencorporates.com/companies/us_al/"

    if numbers not in url_data:
        if counter < 100000:
            counter +=1
            print(numbers)

            url = base_url + numbers
            try:
                entry = ","
                driver.get(url)
                # time.sleep(20)
                uridiction = driver.find_element(by=By.XPATH, value='//*[@id="attributes"]/dl')
                print(uridiction)

                # try:
                #     entry+=url+","
                #     rows = extraction(driver, entry)
                #     print("Rows: ",rows)
                # except Exception as e:
                #     print("Error : ",e)
                #     break

                f.write(url)
                f.write("\n")
                time.sleep(1)
                # break
            except Exception as e:
                f1.write(numbers)
                f1.write('\n')
                print("fail")
                # print(e)
                # break
            # break
        else:
            # time.sleep(300)
            driver.quit()
            # break
