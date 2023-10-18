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

driver.get("https://thegoodshoppingguide.com/brand-directory/aatu/")

time.sleep(5)

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

# sys.exit()

Url = []
name = []
for i in range(1, 13):
    url = 'https://thegoodshoppingguide.com/brand-directory/page/{}/'.format(i)

    driver.get(url)
    time.sleep(2)

    for i in range(1, 13):
        try:
            company_name = driver.find_element(by=By.XPATH, value='//*[@id="main"]/section/div/ul/li[{}]/a'.format(i))
            company_name = company_name.get_attribute('href')
            Url.append(company_name[:-1])
            name.append(company_name[:-1].split('/')[-1].replace('-', ' ').title())
            print(company_name)
            print(company_name[:-1])
            print(company_name[:-1].split('/')[-1].replace('-', ' ').title())
        except:
            company_name = ""

# print(name)

for url in Url:
    li.append(url)

    driver.get(url)
    time.sleep(2)

    try:
        company_name = driver.find_element(by=By.XPATH, value='//*[@id="main"]/article/header/div/div/div[2]/h1')
        print("Company Name : ",company_name.text)
        li1.append(company_name.text)
    except:
        li1.append("")

    try:
        company_name = driver.find_element(by=By.XPATH, value='//*[@id="main"]/article/header/div/div/div[2]/p')
        dict1 = {}
        for i in company_name.text.split('\n'):
            if "Parent" in i:
                print("Parent : ",i.split(':')[1])
                dict1['Parent Company'] =  i.split(':')[1].replace(",", "-")
            
            if "Category" in i:
                print("Category : ",i.split(':')[1])
                dict1['Category'] = i.split(':')[1].replace(",", "-")

        if 'Parent Company' in dict1.keys():
            li2.append(dict1['Parent Company'])
        else:
            li2.append("")
        
        if 'Category' in dict1.keys():
            li3.append(dict1['Category'])
        else:
            li3.append("")
            
    except Exception as e:
        print("Exception--------- : {}".format(e))
        li2.append("")
        li3.append("")

    try:
        company_name = driver.find_element(by=By.XPATH, value='//*[@id="main"]/article/div/div/div[1]/div/div/div/div/p[2]')
        print(company_name.text)
        li4.append(company_name.text)
    except:
        li4.append("")

    try:
        company_name = driver.find_element(by=By.XPATH, value='//*[@id="main"]/article/div/div/div[1]/div/div/div/div/p[5]')
        print(company_name.text)
        li5.append(company_name.text)
    except:
        li5.append("")


    try:
        company_name = driver.find_element(by=By.XPATH, value='//*[@id="main"]/article/div/div/div[1]/div/div/div/div/p[10]')
        print("Sustainable : ",company_name.text)
        li6.append(company_name.text)
    except:
        li6.append("")


    try:
        company_name = driver.find_element(by=By.XPATH, value='//*[@id="main"]/article/div/div/div/div/div/div/div/p[13]')
        print("Ethical Accreditation : ",company_name.text)
        li7.append(company_name.text)
    except:
        li7.append("")

    try:
        company_name = driver.find_element(by=By.XPATH, value='//*[@id="main"]/article/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div')
        print("GSG category benchmark: ",company_name.text)
        li8.append(company_name.text)
    except:
        li8.append("")

    try:
        company_name = driver.find_element(by=By.XPATH, value='//*[@id="main"]/article/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]')
        print("GSG Score: ",company_name.text)
        li9.append(company_name.text)
    except:
        li9.append("")


dict1 = {
    "Url": li,
    "Company Name": li1,
    "Parent Company": li2,
    "Category": li3,
    "Ethical Company": li4,
    "Well Performed": li5,
    "Sustainable": li6,
    "Ethical Accreditation": li7,
    "GSG Category benchmark": li8,
    "GSG Score": li9
}

print(dict1)

df = pd.DataFrame(dict1)
df.to_csv('Good_Shopping_Guide_Ethical_Award.csv')
