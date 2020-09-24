from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import sys
import regex as re
import requests as re
from bs4 import BeautifulSoup as bs

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver= webdriver.Chrome(options=chrome_options, executable_path="E:\Scrapper\Scrapping\Scrapper\chromedriver.exe")

what_keyword = ["Transformation", "Business Analyst", "Process", "Code of practice", "Regulation"]

where = ["Sydney", "Melbourne", "Brisbane"]

company_blacklist = pd.read_excel("E:\Scrapper\Scrapping\Scrapper\company_blacklist.xlsx").Company.tolist()

company_whitelist = pd.read_excel("E:\Scrapper\Scrapping\Scrapper\company_whitelist.xlsx").Company.tolist()

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

job_title, companies, domain, links, industry, company_mark = [],[],[],[],[],[]
dummy_links = []
for what in what_keyword:
    for city in where:
        base_url = "https://www.linkedin.com/jobs/search/?geoId=104468365&keywords="
        base_url+=what.lower().replace(" ", "%20")
        base_url+="&location="+city.replace(" ", "-")
        print(base_url)

        # driver.get(base_url)

        for page in range(0,400,25):
            url = base_url+"&start="+str(page)
            print(url)

            res = re.get(url, headers=headers)

            soup = bs(res.text, 'lxml')

            job_result = soup.find_all('li', class_='result-card job-result-card result-card--with-hover-state')

            for item in job_result:
                
                Job_link = item.find('a').get('href')
                if Job_link not in dummy_links:
                    Job_name = item.find('h3').text

                    try:
                        Job_company = item.find('h4').find('a').text
                    except:
                        Job_company = item.find('h4').text

                    driver.get(Job_link)
                    index = 0
                    try:
                        data = driver.find_element_by_xpath("//section[@class='core-rail']//section[@class='description']").text

                        _data = data.split("\n")
                        index = _data.index("Industries")
                        
                        if len(_data[index+1].split("Staffing and Recruiting")) == 1:
                            indust = _data[index+1]

                            if Job_company in company_blacklist:
                                    print("Blacklisted----->",Job_company)
                            elif Job_company in company_whitelist:
                                companies.append(Job_company)                        
                                job_title.append(Job_name)
                                dummy_links.append(Job_link)
                                links.append(Job_link)
                                domain.append("LinkedIN")
                                industry.append(indust)
                                company_mark.append("1")

                                print("*"*120)
                                print("Whitelisted Company---------------------Whitelisted")
                                print("Job Name------->",Job_name)
                                print("Job Link------->",Job_link)
                                print("Job Comp,any---->",Job_company)
                                print("Job Industry--->",indust)
                                print("*"*120)
                                print()
                                print()

                            else:
                                companies.append(Job_company)                        
                                job_title.append(Job_name)
                                dummy_links.append(Job_link)
                                links.append(Job_link)
                                domain.append("LinkedIN")
                                industry.append(indust)
                                company_mark.append("")

                                print("*"*120)
                                print("Job Name------->",Job_name)
                                print("Job Link------->",Job_link)
                                print("Job Comp,any---->",Job_company)
                                print("Job Industry--->",indust)
                                print("*"*120)
                                print()
                                print()
                    except Exception as e:
                        print("Error----------->",e)

                else:
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>Duplicate>>>>>>>>>>>>")

print()
print()
print("Lenth of companies--->",len(companies))
print("Length of job_title-->",len(job_title))
print("Length of links------>",len(links))
print("Length of domain----->",len(domain))
print("Length of industry--->",len(industry))

df = pd.DataFrame({"Job Title": job_title, "Company": companies, "company_mark":company_mark, "Industry":industry, "Domain":domain, "Link":links})
print(df.head())

df.to_excel("LinkedIN_data.xlsx")


