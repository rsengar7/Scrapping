from __future__ import print_function
from bs4 import BeautifulSoup as bs
import requests as req 
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import sys
import regex as re

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver= webdriver.Chrome(options=chrome_options, executable_path="/home/ritesh/Videos/Jason/Scrapper/chromedriver")


class Scrape:

    save_file = []
    
    headers = {
    'authority': 'www.linkedin.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
    }


    
    def crawl(self,url):

        while True:

            try:
                res = req.get(url, headers=self.headers)
                self.parse(res.text)
                break

            except:
                print('connection lost')

    def parse(self, html_text):

        soup = bs(html_text, 'lxml')

        job_result = soup.find_all('li', class_='result-card job-result-card result-card--with-hover-state')

        for item in job_result:
            
            Job_link = item.find('a').get('href')
            Job_name = item.find('h3').text

            try:
                Job_company = item.find('h4').find('a').text
            except:
                Job_company = item.find('h4').text

            driver.get(Job_link)
            data = driver.find_element_by_xpath("//section[@class='core-rail']//section[@class='description']").text

            _data = data.split("\n")
            index = _data.index("Industries")

            print("Job Name------->",Job_name)
            print("Job Link------->",Job_link)
            print("Job Comp,any---->",Job_company)
            if len(_data[index+1].split("Staffing and Recruiting")) > 1:
                print("Job Industry--->",_data[index+1])

start = Scrape()


for page in range(0,950,25):

    url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?currentJobId=2012714430&geoId=104468365&keywords=change&location=Brisbane&start=' + str(page)
    start.crawl(url)
    sys.exit()
