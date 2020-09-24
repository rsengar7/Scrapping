from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import sys
import regex as re

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver= webdriver.Chrome(options=chrome_options, executable_path="/home/ritesh/Videos/Jason/Scrapper/Seek/chromedriver")

what_keyword = ["Change Manager", "change", "Business Transformation", "Project Manager", "PMO", "Agility", "Agile", "Transformation", "Business Analyst", "Process", "Code of practice", "Regulation"]

where = ["Sydney", "Melbourne", "Brisbane"]

company_blacklist = pd.read_excel("/home/ritesh/Videos/Jason/Scrapper/company_blacklist.xlsx").Company.tolist()

job_title, company, domain, link, industry = [],[],[],[],[]

for what in what_keyword:
    for city in where:
        base_url = "https://www.seek.com.au/"
        base_url+=what.lower().replace(" ", "-")+"-jobs"
        base_url+="/in-"+city.replace(" ", "-")+"/contract-temp?daterange=7"
        print(base_url)

        for page in range(0,31):
            url = base_url+"&page="+str(page)
            print(url)
            driver.get(url)

            articles = driver.find_elements_by_tag_name('article')

            if len(articles) > 0:
                for index, article in enumerate(articles):
                    _data = article.text.split("\n")
                    if _data[4] not in company_blacklist:
                        for i in _data:
                            y = re.search('^classification', i)
                            if(y!=None):
                                x_path=re.findall("\classification: [a-zA-Z0-9\s\&,]+", i)
                                if (x_path):
                                    industry.append(x_path[0].split("\n")[0].split(":")[1].strip())
                                else:
                                    industry.append("")

                        job_title.append(_data[0])
                        company.append(_data[4])
                        domain.append("Seek")
                        link.append(article.find_element_by_tag_name('a').get_attribute("href"))
                    else:
                        print("Blacklisted------->>",_data[4])

df = pd.DataFrame({"Job Title": job_title, "Company": company, "Industry":industry, "Domain":domain, "Link":link})
print(df.head())

df.to_excel("seek_data_updated.xlsx")
