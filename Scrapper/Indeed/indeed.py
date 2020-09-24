import pandas as pd
import sys
from bs4 import BeautifulSoup as bs
import requests as re

what_keyword = ["Change Manager", "change", "Business Transformation", "Project Manager", "PMO", "Agility", "Agile", "Transformation", "Business Analyst", "Process", "Code of practice", "Regulation", "Aviation & Travel", "Banking & Financial Services", "Customer Service", "Energy & Renewables", "FMCG", "Food & Agriculture", "Health", "Insurance", "Not for Profit", "Public Services", "Retail", "Software & Technology", "Telecommunications"]

where = ["Sydney", "Melbourne", "Brisbane"]

company_blacklist = pd.read_excel("/home/ritesh/Videos/Jason/Scrapper/company_blacklist.xlsx").Company.tolist()

job_title, companies, domain, links, industry = [],[],[],[],[]
dummy_links = []
for what in what_keyword:
    for city in where:
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
                    else:
                        companies.append(company)                        
                        job_title.append(name)
                        dummy_links.append(link)
                        links.append(link)
                        domain.append("Indeed")
                        industry.append("")


df = pd.DataFrame({"Job Title": job_title, "Company": companies, "Industry":industry, "Domain":domain, "Link":link})
print(df.head())

df.to_excel("indeed_data.xlsx")