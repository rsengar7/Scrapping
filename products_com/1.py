"""

{
	"tv": {
		"url": "https://productz.com/en/tvs/c/48",
		"page": 166
	},
	"headphones": {
		"url": "https://productz.com/en/headphones/c/47",
		"page": 166
	},
	"refrigerators": {
		"url": "https://productz.com/en/refrigerators/c/43",
		"page": 166
	},
	"routers": {
		"url": "https://productz.com/en/routers/c/144",
		"page": 42
	},
	"childcarseats": {
		"url": "https://productz.com/en/child-car-seats/c/135",
		"page": 12
	},
	"digitalcameras": {
		"url": "https://productz.com/en/digital-cameras/c/3",
		"page": 66
	},
	"electricscooters": {
		"url": "https://productz.com/en/electric-scooters/c/280",
		"page": 4
	},
	"mobilephones": {
		"url": "https://productz.com/en/mobile-phones/c/50",
		"page": 149
	},
	"wirelessspeakers": {
		"url": "https://productz.com/en/wireless-speakers/c/57",
		"page": 140
	},
	"monitors": {
		"url": "https://productz.com/en/monitors/c/103",
		"page": 166
	},
	"projectors": {
		"url": "https://productz.com/en/projectors/c/91",
		"page": 102
	},
	"washers": {
		"url": "https://productz.com/en/washers/c/45",
		"page": 166
	},
	"roboticcleaners": {
		"url": "https://productz.com/en/robotic-cleaners/c/64",
		"page": 11
	}
}

"""

import time, sys, os
import wget
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from csv import writer

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# driver= webdriver.Chrome(options=chrome_options, executable_path='C:\\Users\\rseng\\OneDrive\\Documents\\Office Lens\\Videos\\WorkBook\\Imogen&Jay\\Scrapping\\chromedriver.exe')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# //*[@id="products-filters-container"]/div/div[2]/a[2]

for i in range(1, 137):
    url = 'https://productz.com/en/mice/c/117/'+str(i)

    driver.get(url)

    # /html/body/section/div/div/ol/li[2]/button
    time.sleep(3)
    Company = []
    Product = []
    ProductUrl = []
    OR = []
    NoB = []
    ToMS = []

    for j in range(1, 61):
        try:
            company_name = driver.find_element_by_xpath('//*[@id="products-filters-container"]/div/div[2]/a[{}]/span[2]'.format(str(j)))
            company_name = company_name.text
        except:
            company_name = ""
        
        try:
            product_name = driver.find_element_by_xpath('//*[@id="products-filters-container"]/div/div[2]/a[{}]/p'.format(str(j)))
            product_name = product_name.text
        except:
            product_name = ""
        
        try:
            product_url = driver.find_element_by_xpath('//*[@id="products-filters-container"]/div/div[2]/a[{}]'.format(str(j)))
            product_url = product_url.get_attribute('href')
        except:
            product_url = ""

        try:
                                                               # //*[@id="products-filters-container"]/div/div[2]/a[1]/ul/li[1]
            operating_resolution = driver.find_element_by_xpath('//*[@id="products-filters-container"]/div/div[2]/a[{}]/ul/li[1]'.format(str(j)))
            operating_resolution = operating_resolution.text.sp
        except:
            operating_resolution = ""
        
        try:        
                                                        # //*[@id="products-filters-container"]/div/div[2]/a[1]/ul/li[2]
            num_of_buttons = driver.find_element_by_xpath('//*[@id="products-filters-container"]/div/div[2]/a[{}]/ul/li[2]'.format(str(j)))
            num_of_buttons = num_of_buttons.text
        except:
            num_of_buttons = ""

        try:    
                                                                # //*[@id="products-filters-container"]/div/div[2]/a[1]/ul/li[4]
                                                                # //*[@id="products-filters-container"]/div/div[2]/a[1]/ul/li[3]
            type_of_motion_sensor = driver.find_element_by_xpath('//*[@id="products-filters-container"]/div/div[2]/a[{}]/ul/li[3]'.format(str(j)))
            type_of_motion_sensor = type_of_motion_sensor.text
        except:
            type_of_motion_sensor = ""

        print("Company Name : ",company_name)
        print("product_name : ",product_name)
        print("product_url  : ",product_url)
        print("operating_resolution : ",operating_resolution)
        print("num_of_buttons : ",num_of_buttons)
        print("type_of_motion_sensor : ",type_of_motion_sensor)

        break
    break



    dict1 = {
        "Company Name": company_name,
        ""
    }
        

    