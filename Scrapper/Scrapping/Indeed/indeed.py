import pandas as pd
import sys
from bs4 import BeautifulSoup as bs
import requests as re

what_keyword = ["Change Manager", "change", "Business Transformation", "Project Manager", "PMO", "Agility", "Agile", "Transformation", "Business Analyst", "Process", "Code of practice", "Regulation", "Aviation & Travel", "Banking & Financial Services", "Customer Service", "Energy & Renewables", "FMCG", "Food & Agriculture", "Health", "Insurance", "Not for Profit", "Public Services", "Retail", "Software & Technology", "Telecommunications"]

where = ["Sydney", "Melbourne", "Brisbane"]

company_blacklist = ['Illuminate Search & Consulting', 'Paxus', 'Chandler Macleod Group', 'Ash Executive', 'SustainAbility Consulting', 'Ashdown People', 'Peoplebank Australia NSW', 'u&u. Recruitment Partners', 'PMWorks Pty Ltd', 'Robert Walters', 'Allura Partners', 'T+O+M Executive', 'AJQ', 'Talent – Winner ‘Seek Large Recruitment Agency of the Year’ 3 consecutive years!', 'Bluefin Resources Pty Limited', 'First People Recruitment Solutions Pty Ltd', 'Hudson - Project Services', 'Next Day Recruitment', 'Clicks IT Recruitment (ACT)', 'Hawksworth Consulting', 'Hays Information Technology', 'Beaumont People', 'Precision Sourcing', 'Randstad Technologies', 'Lanson Partners', 'Finite IT Recruitment Solutions', 'Aurec', 'Michael Page Information Technology', 'Greythorn Experis', 'ecareer employment services', 'Orchard HRO', 'HR Partners – Sydney', 'Callaways', 'Richard Lloyd Accounting Recruitment', 'FinXL IT Professional Services', 'Michael Page Human Resources', 'B & K Consulting', 'Hays Human Resources', 'Sirius Technology Sydney part of Sirius People Pty Ltd', 'Dynamo Recruitment', 'TalentWeb Consulting', 'FutureYou', 'HCM Australia', 'Balance Recruitment', 'SALT SEARCH PTY LTD', 'Modis', 'Randstad - Banking & Finance', 'Talenza', 'Charterhouse', 'Ethos BeathChapman', 'ProjectSource', '2XM Technology Pty Ltd', 'Ampersand International', 'Interface Agency', '2XM Recruit', 'Connect One Recruitment', 'Profusion PAC Pty Ltd', 'Hays Talent Solutions', 'Launch Recruitment Pty Ltd', 'people2people - Sydney', 'GRIT Talent Consulting', 'Allan Hall HR', 'First Grade Recruitment', 'M&T Resources']

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