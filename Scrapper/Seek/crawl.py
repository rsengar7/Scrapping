from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date, timedelta
import time
import logging
import argparse, sys
import pandas as pd
import regex as re

log = logging.getLogger(__name__)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver= webdriver.Chrome(options=chrome_options, executable_path="/home/ritesh/Videos/Jason/Scrapper/chromedriver")

company_blacklist = ['Illuminate Search & Consulting', 'Paxus', 'Chandler Macleod Group', 'Ash Executive', 'SustainAbility Consulting', 'Ashdown People', 'Peoplebank Australia NSW', 'u&u. Recruitment Partners', 'PMWorks Pty Ltd', 'Robert Walters', 'Allura Partners', 'T+O+M Executive', 'AJQ', 'Talent – Winner ‘Seek Large Recruitment Agency of the Year’ 3 consecutive years!', 'Bluefin Resources Pty Limited', 'First People Recruitment Solutions Pty Ltd', 'Hudson - Project Services', 'Next Day Recruitment', 'Clicks IT Recruitment (ACT)', 'Hawksworth Consulting', 'Hays Information Technology', 'Beaumont People', 'Precision Sourcing', 'Randstad Technologies', 'Lanson Partners', 'Finite IT Recruitment Solutions', 'Aurec', 'Michael Page Information Technology', 'Greythorn Experis', 'ecareer employment services', 'Orchard HRO', 'HR Partners – Sydney', 'Callaways', 'Richard Lloyd Accounting Recruitment', 'FinXL IT Professional Services', 'Michael Page Human Resources', 'B & K Consulting', 'Hays Human Resources', 'Sirius Technology Sydney part of Sirius People Pty Ltd', 'Dynamo Recruitment', 'TalentWeb Consulting', 'FutureYou', 'HCM Australia', 'Balance Recruitment', 'SALT SEARCH PTY LTD', 'Modis', 'Randstad - Banking & Finance', 'Talenza', 'Charterhouse', 'Ethos BeathChapman', 'ProjectSource', '2XM Technology Pty Ltd', 'Ampersand International', 'Interface Agency', '2XM Recruit', 'Connect One Recruitment', 'Profusion PAC Pty Ltd', 'Hays Talent Solutions', 'Launch Recruitment Pty Ltd', 'people2people - Sydney', 'GRIT Talent Consulting', 'Allan Hall HR', 'First Grade Recruitment', 'M&T Resources']

for page in range(0,50):
    try:
        driver.get("https://www.seek.com.au/project-manager-jobs/in-All-Brisbane-QLD/contract-temp?page="+str(page))

        articles = driver.find_elements_by_tag_name('article')
        if len(articles) > 0:

            job_title, company, domain, link, industry = [],[],[],[],[]

            for index, article in enumerate(articles):
                # print(article.text)
                
                print("*"*80)
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

            df = pd.DataFrame({"Job Title": job_title, "Company": company, "Industry": industry, "Domain":domain, "Link":link})
            print(df.head(15))
            # print()

            sys.exit()
        else:
            break
    except Exception as e:
        print("^"*80)
        print("Error---------->",e)
        print("^"*80)


# ActionChains(driver).move_to_element(article).perform()
# if article.find_element_by_tag_name('a').text == "sold out":
#      print("sold out")
#      link = article.find_element_by_xpath('div/a').get_attribute('href')
#      print(link)
# else:
#      print("available")



# import pandas as pd

# df = pd.read_excel("seek_data.xlsx")
# print(df.info())
# print()
# print(df.head())


# import re

# txt =["Cyber Security Project Manager", "Listed seventeen days ago", "classification: Information & Communication Technology", "Information & Communication Technology","Programme & Project Management","Save"]

# #Check if "Portugal" is in the string:
# for i in txt:
#   x = re.findall("classification: [a-zA-Z0-9\s \&]+", i)
#   print(x)

#   if (x):
#     print("Yes, there is at least one match!")
#     print(x[0].split(":")[1].strip())
  
