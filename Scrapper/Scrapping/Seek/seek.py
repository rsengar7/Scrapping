from __future__ import print_function
import os, sys
import regex as re
import csv
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from dotenv import load_dotenv

load_dotenv()

try:
    BLACKLIST_DIR = os.environ["BLACKLIST_DIR"]
    WHITELIST_DIR = os.environ["WHITELIST_DIR"]
    LOGS_DIR = os.environ["LOGS_DIR"]
    CHROME_DRIVER = os.environ["CHROME_DRIVER"]

except Exception as e:
    print("Error-------->",e)
    sys.exit()

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver= webdriver.Chrome(options=chrome_options, executable_path=CHROME_DRIVER)

where = ["Sydney", "Melbourne", "Brisbane"]

company_blacklist = pd.read_excel(BLACKLIST_DIR).Company.tolist()

company_whitelist = pd.read_excel(WHITELIST_DIR).Company.tolist()

_where = ['Sydney']
writers = pd.ExcelWriter('Seek_data.xlsx')

for title in ["Ecosystem Log", "Renforce", "Insight X"]:
    df = pd.read_excel(LOGS_DIR+""+title+".xlsx")
    what_keyword = df.Keyword.tolist()[:1]

    print(what_keyword)

    job_title, companies, domain, links, industry, company_mark = [],[],[],[],[],[]

    for what in what_keyword:
        for city in _where:
            base_url = "https://www.seek.com.au/"
            base_url+=what.lower().replace(" ", "-")+"-jobs"
            base_url+="/in-"+city.replace(" ", "-")+"/contract-temp?daterange=7"
            print(base_url)

            for page in range(1,31):
                url = base_url+"&page="+str(page)
                print(url)
                driver.get(url)

                articles = driver.find_elements_by_tag_name('article')

                if len(articles) > 0:
                    for index, article in enumerate(articles):
                        _data = article.text.split("\n")
                        x_path = False
                        for i in _data:
                                y = re.search('^classification', i)
                                if(y!=None):
                                    x_path=re.findall("\classification: [a-zA-Z0-9\s\&,]+", i)

                        if _data[4] not in company_blacklist:
                            if (x_path):
                                industry.append(x_path[0].split("\n")[0].split(":")[1].strip())
                            else:
                                industry.append("")

                            job_title.append(_data[0])
                            companies.append(_data[4])
                            domain.append("Seek")
                            links.append(article.find_element_by_tag_name('a').get_attribute("href"))
                            company_mark.append("")
                        elif _data[4] in company_whitelist:
                            if (x_path):
                                industry.append(x_path[0].split("\n")[0].split(":")[1].strip())
                            else:
                                industry.append("")

                            job_title.append(_data[0])
                            companies.append(_data[4])
                            domain.append("Seek")
                            links.append(article.find_element_by_tag_name('a').get_attribute("href"))
                            company_mark.append("1")

                        else:
                            print("Blacklisted------->>",_data[4])

    df = pd.DataFrame({"Job Title": job_title, "Company": companies, "company_mark":company_mark, "Industry":industry, "Domain":domain, "Link":links})
    print(df.head())

    df.to_csv("seek.csv")

    Final = []

    with open('seek.csv','r') as linked:

        read = csv.reader(linked)

        for item in read:
            print(item)
            if item not in Final:
                Final.append(item)

    time.sleep(2)
    print("Length of Collected Data ---------->",len(df))
    os.remove('seek.csv')

    with open('Final.csv','w',newline='') as final:

        w = csv.writer(final)

        for item in Final:
            w.writerow(item)

    print("Lenth of Final After Removal of Duplicate ---->",len(Final))
    df1 = pd.read_csv("Final.csv")
    print("Length of Final Csv After Reading------------->",len(df1))

    df1.to_excel(writers, title)
    time.sleep(2)
    os.remove("Final.csv")

    del df
    del df1

writers.save()
