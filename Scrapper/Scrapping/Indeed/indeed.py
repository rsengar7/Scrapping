import os, sys
import requests as re
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup as bs

from dotenv import load_dotenv

load_dotenv()

try:
    BLACKLIST_DIR = os.environ["BLACKLIST_DIR"]
    WHITELIST_DIR = os.environ["WHITELIST_DIR"]
    LOGS_DIR = os.environ["LOGS_DIR"]

except Exception as e:
    print("Error-------->",e)
    sys.exit()

where = ["Sydney", "Melbourne", "Brisbane"]

company_blacklist = pd.read_excel(BLACKLIST_DIR).Company.tolist()

company_whitelist = pd.read_excel(WHITELIST_DIR).Company.tolist()

_where = ["Sydney"]

writers = pd.ExcelWriter('Indeed_data.xlsx')

for title in ["Ecosystem Log", "Renforce", "Insight X"]:
    df = pd.read_excel(LOGS_DIR+""+title+".xlsx")
    what_keyword = df.Keyword.tolist()[:1]

    job_title, companies, domain, links, industry, company_mark = [],[],[],[],[],[]
    dummy_links = []

    for what in what_keyword:
        for city in _where:
            base_url = "https://au.indeed.com/jobs?q="
            base_url+=what.replace(" ", "+")
            base_url+="&l="+city.replace(" ", "+")+"&jt=contract&fromage=7"
            print(base_url)

            for page in range(0,100,10):
                url = base_url+"&start="+str(page)
                print(url)

                res = re.get(url)

                soup = bs(res.text, 'lxml')
                
                h2 = soup.find_all('div', {'data-tn-component':'organicJob'})

                for item in h2:
                    name = item.find('a').get('title')
                    link = 'https://au.indeed.com' + item.find('a').get('href')
                    if link not in dummy_links:
                        try:
                            company = item.find('a', {'data-tn-element':'companyName'}).text.strip()
                        except AttributeError:
                            company = item.find('div', class_='sjcl').find('span').text.strip()

                        if company in company_blacklist:
                            print("Blacklisted----->",company)
                        elif company in company_whitelist:
                            companies.append(company)                        
                            job_title.append(name)
                            dummy_links.append(link)
                            links.append(link)
                            domain.append("Indeed")
                            industry.append("")
                            company_mark.append("1")
                        else:
                            companies.append(company)                        
                            job_title.append(name)
                            dummy_links.append(link)
                            links.append(link)
                            domain.append("Indeed")
                            industry.append("")
                            company_mark.append("")


    df = pd.DataFrame({"Job Title": job_title, "Company": companies, "company_mark":company_mark, "Industry":industry, "Domain":domain, "Link":links})
    print(df.head())

    df.to_csv("indeed.csv")

    Final = []

    with open('indeed.csv','r') as linked:

        read = csv.reader(linked)

        for item in read:
            print(item)
            if item not in Final:
                Final.append(item)

    time.sleep(2)
    print("Length of Collected Data ---------->",len(df))
    os.remove('indeed.csv')

    with open('Final.csv','w',newline='') as final:

        w = csv.writer(final)

        for item in Final:
            w.writerow(item)

    print("Lenth of Final After Removal of Duplicate ---->",len(Final))
    df1 = pd.read_csv("Final.csv")
    print("Length of Final Csv After Reading------------->",len(df1))
    print("Title----------->",title)
    df1.to_excel(writers, title)
    time.sleep(2)
    os.remove("Final.csv")

    del df
    del df1

writers.save()
