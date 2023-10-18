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

driver.get('https://declare.living-future.org/')

time.sleep(3)

# company_name = '//*[@id="thumbnail-flex-box"]/a[1]/div[2]/div/h6'
# '//*[@id="thumbnail-flex-box"]/a[2]/div[2]/div/h6'

# product_name = '//*[@id="thumbnail-flex-box"]/a[1]/div[2]/div/h3'
# '//*[@id="thumbnail-flex-box"]/a[2]/div[2]/div/h3'

# '//*[@id="thumbnail-flex-box"]/a[27]/div[2]/div/h3'

# while True:
Products = []
Companys = []
Urls = []
for i in range(1, 100):

    Y = i*4000
    product_name = driver.find_elements(by=By.TAG_NAME, value='h3')
    company_name = driver.find_elements(by=By.TAG_NAME, value='h6')

    for index, product in enumerate(product_name):
        prod = " ".join([i.strip('™').strip('®') for i in product.text.split(" ")])
        if prod not in Products:
            print(prod)
            Products.append(prod)
            print(company_name[index].text)
            Companys.append(company_name[index].text)
            url = "https://declare.living-future.org/products/"+prod.lower().replace(" ", "-").replace("/", "-").replace(".","").replace(",", "-").replace("&", "").replace(":", "").replace("(", "").replace(")", "").replace("+", "")
            print(url)
            Urls.append(url)

    print()

    driver.execute_script("window.scrollTo(0, {})".format(Y)) 
    
    time.sleep(2)

# time.sleep(30)

df = pd.DataFrame({"URL": Urls, "Product": Products, "Company": Companys})
df.to_csv("declare-living.csv")