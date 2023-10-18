import time, sys, os
import wget
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from csv import writer

import io
import requests
import pytesseract
from PIL import Image

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('headless')


flag = 0

for files in os.listdir("glassdoor_top_CEO20"):
    print(files)
    if files != "glassdoor_top_CEO2013.csv" and files != "glassdoor_top_CEO2014.csv":
        url_li = []
        websites = []
        size = []
        types = []
        revenue = []
        headquarter = []
        founded = []
        industries = []
        description = []

        df = pd.read_csv("glassdoor_top_CEO20/"+files)
        urls = df['ceoProfileUrl'].values.tolist()

        for index, url in enumerate(urls):
            driver= webdriver.Chrome(options=chrome_options, executable_path='/home/ritesh/Videos/WorkBook/Imogen&Jay/Scrapping/chromedriver')

            try:
                print(url)
                url_li.append(url)

                driver.get(url)
                # if flag == 0:
                #     flag+= 1
                #     time.sleep(10)

                try:
                    wesbite = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[1]/a')
                    websites.append(wesbite.text)
                except:
                    websites.append("")
                
                try:
                    company_size = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[3]/div')
                    size.append(company_size.text)
                except:
                    size.append("")
                
                try:
                    company_type = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[5]/div')
                    types.append(company_type.text)
                except:
                    types.append("")
                
                try:
                    comapny_revenue = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[7]/div')
                    revenue.append(comapny_revenue.text)
                except:
                    revenue.append("")
                
                try:
                    company_headquarter = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[2]/div')
                    headquarter.append(company_headquarter.text)
                except:
                    headquarter.append("")
                
                try:
                    company_founded = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[4]/div')
                    founded.append(company_founded.text)
                except:
                    founded.append("")
                
                try:
                    industry = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[6]/a')
                    industries.append(industry.text)
                except:
                    industries.append("")

                try:
                    button = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/div/span/button')
                    button.click()
                    comapny_description = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/div[1]/span')
                    description.append(comapny_description.text)
                except:
                    description.append("")

                print(wesbite.text)
                print("------------")
                print(company_size.text)
                print("------------")
                print(company_type.text)
                print("------------")
                print(comapny_revenue.text)
                print("------------")
                print(company_headquarter.text)
                print("------------")
                print(company_founded.text)
                print("------------")
                print(industry.text)
                print("------------")
                print(comapny_description.text)
                driver.close()
                # break
            except Exception as e:
                print("Error ----->",e)
                driver.close()

        jsons = {
            "URL": url_li,
            "Website": websites,
            "Size": size,
            "Type": types,
            "Revenue": revenue,
            "HeadQuarter": headquarter,
            "Founded": founded,
            "Industry": industries,
            "Description": description
        }

        df = pd.DataFrame(jsons)

        df.to_csv("Part_CEO/1_"+files)
        # break

    # driver.get(url)
