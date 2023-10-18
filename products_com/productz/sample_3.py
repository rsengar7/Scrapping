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

Company = []
Product = []
ProductUrl = []
ScreenSize = []
Resolutions = []
SmartTV = []
WIFI = []


slap1 = "Touchscreen"
slap2 = "Colour screen"
slap3 = "GPS"
pages = 22
csvname = "FitnessWatches.csv"
urlname = "https://productz.com/en/fitness-watches/c/101"

screen_size_var = ""
resolution_var = ""
smart_tv_var = ""
wifi_var = ""

for i in range(1, pages):
    url = urlname+'/'+str(i)

    driver.get(url)
    time.sleep(1)

    try:
        button = driver.find_element(by=By.XPATH, value='/html/body/section/div/div/ol/li[2]/button')
        button.click()

        time.sleep(2)
    except:
        pass

    for j in range(1, 61):
        try:
            company_name = driver.find_element(by=By.XPATH, value='//*[@id="products-filters-container"]/div/div[2]/a[{}]/span[2]'.format(str(j)))
            company_name = company_name.text
        except:
            company_name = ""
        
        try:
            product_name = driver.find_element(by=By.XPATH, value='//*[@id="products-filters-container"]/div/div[2]/a[{}]/p'.format(str(j)))
            product_name = product_name.text
        except:
            product_name = ""
        
        try:
            product_url = driver.find_element(by=By.XPATH, value='//*[@id="products-filters-container"]/div/div[2]/a[{}]'.format(str(j)))
            product_url = product_url.get_attribute('href')
        except:
            product_url = ""

        try:
            screen_size = driver.find_element(by=By.XPATH, value='//*[@id="products-filters-container"]/div/div[2]/a[{}]/ul/li[1]'.format(str(j)))
            screen_size = screen_size.text.split(":")

            if screen_size[0] == slap1:
                screen_size_var = screen_size[1]
            elif screen_size[0] == slap2:
                resolution_var = screen_size[1]
            elif screen_size[0] == slap3:
                smart_tv_var = screen_size[1]
            else:
                pass

        except:
            screen_size_var = ""
        
        try:
            resolution = driver.find_element(by=By.XPATH, value='//*[@id="products-filters-container"]/div/div[2]/a[{}]/ul/li[2]'.format(str(j)))
            resolution = resolution.text.split(":")

            if resolution[0] == slap2:
                resolution_var = resolution[1]
            elif resolution[0] == slap3:
                smart_tv_var = resolution[1]
            else:
                pass
        except:
            resolution_var = ""

        try:    
            smart_tv = driver.find_element(by=By.XPATH, value='//*[@id="products-filters-container"]/div/div[2]/a[{}]/ul/li[3]'.format(str(j)))
            smart_tv = smart_tv.text.split(":")

            if smart_tv[0] == slap3:
                smart_tv_var = smart_tv[1]
        except:
            smart_tv_var = ""



        print("Company Name===",company_name)
        print("product_name===",product_name)
        print("product_url===",product_url)
        print(slap1,"===",screen_size_var)
        print(slap2,"===",resolution_var)
        print(slap3,"===",smart_tv_var)
        print()
        print()

        Company.append(company_name)
        Product.append(product_name)
        ProductUrl.append(product_url)
        ScreenSize.append(screen_size_var)
        Resolutions.append(resolution_var)
        SmartTV.append(smart_tv_var)


dict1 = {
    "Product Url": ProductUrl,
    "Product Name": Product,
    "Company Name": Company
}

dict1[slap1] = ScreenSize
dict1[slap2] = Resolutions
dict1[slap3] = SmartTV


df = pd.DataFrame(dict1)

df.to_csv(csvname)
    