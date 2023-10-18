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

df = pd.read_csv('blauer-engel.csv')

# links = df['Links'].values.tolist()
# names = df['Names'].values.tolist()

data = df.values.tolist()

counter = 0
for index, row in enumerate(data):
    row[1] = row[1].replace("/", "-")
    
    if not os.path.isfile("Pdf/"+row[1]+".pdf"):
        try:
            # if index == 2:
            #     break
            print("Row : ",row)
            print(len(data),"---",index) 
            driver.get(row[2])

            button = driver.find_element(by=By.XPATH, value='//*[@id="edit-submit-pdf"]')
            driver.execute_script("arguments[0].click();", button)

            time.sleep(5)

            print("Name : ",row[1])
            row[1] = row[1].replace("/", "-")
            print("Name : ",row[1])

            if os.path.isfile('C:\\Users\\rseng\\Downloads\\BlauerEngel.pdf'):
                print("Exist")
                os.rename('C:\\Users\\rseng\\Downloads\\BlauerEngel.pdf', 'C:\\Users\\rseng\\Downloads\\Pdf\\'+row[1]+".pdf")
            else:
                time.sleep(5)
                if os.path.isfile('C:\\Users\\rseng\\Downloads\\BlauerEngel.pdf'):
                    print("Exist")
                    os.rename('C:\\Users\\rseng\\Downloads\\BlauerEngel.pdf', 'C:\\Users\\rseng\\Downloads\\Pdf\\'+row[1]+".pdf")
                else:
                    time.sleep(5)
                    if os.path.isfile('C:\\Users\\rseng\\Downloads\\BlauerEngel.pdf'):
                        print("Exist")
                        os.rename('C:\\Users\\rseng\\Downloads\\BlauerEngel.pdf', 'C:\\Users\\rseng\\Downloads\\Pdf\\'+row[1]+".pdf")
                    else:
                        time.sleep(5)
                        if os.path.isfile('C:\\Users\\rseng\\Downloads\\BlauerEngel.pdf'):
                            print("Exist")
                            os.rename('C:\\Users\\rseng\\Downloads\\BlauerEngel.pdf', 'C:\\Users\\rseng\\Downloads\\Pdf\\'+row[1]+".pdf")
                        else:
                            pass
        except:
            pass

    if not os.path.isfile("Excel/"+row[1]+".xlsx"):
        try:
            button = driver.find_element(by=By.XPATH, value='//*[@id="edit-submit-xlsx"]')
            driver.execute_script("arguments[0].click();", button)

            row[1] = row[1].replace('/', "-")

            if os.path.isfile('C:\\Users\\rseng\\Downloads\\Blue_Angel_2022-10-22.xlsx'):
                print("Exist")
                os.rename('C:\\Users\\rseng\\Downloads\\Blue_Angel_2022-10-22.xlsx', 'C:\\Users\\rseng\\Downloads\\Excel\\'+row[1]+".xlsx")
            else:
                time.sleep(5)
                if os.path.isfile('C:\\Users\\rseng\\Downloads\\Blue_Angel_2022-10-22.xlsx'):
                    print("Exist")
                    os.rename('C:\\Users\\rseng\\Downloads\\Blue_Angel_2022-10-22.xlsx', 'C:\\Users\\rseng\\Downloads\\Excel\\'+row[1]+".xlsx")
                else:
                    time.sleep(5)
                    if os.path.isfile('C:\\Users\\rseng\\Downloads\\Blue_Angel_2022-10-22.xlsx'):
                        print("Exist")
                        os.rename('C:\\Users\\rseng\\Downloads\\Blue_Angel_2022-10-22.xlsx', 'C:\\Users\\rseng\\Downloads\\Excel\\'+row[1]+".xlsx")
                    else:
                        time.sleep(5)
                        if os.path.isfile('C:\\Users\\rseng\\Downloads\\Blue_Angel_2022-10-22.xlsx'):
                            print("Exist")
                            os.rename('C:\\Users\\rseng\\Downloads\\Blue_Angel_2022-10-22.xlsx', 'C:\\Users\\rseng\\Downloads\\Excel\\'+row[1]+".xlsx")
                        else:
                            pass
        except: pass
    else: pass

