import time, sys, os
import wget
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
from csv import writer

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# driver.get("https://ccc.bc.edu/ccc/membership/member-list.html")

URL = "https://rioscertification.org/find-a-rios-recycler/"

driver.get(URL)

# headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
# # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link.
# req = requests.get(url=URL, headers=headers)
# # print(req.content)

# soup = BeautifulSoup(req.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
# # print(soup.prettify())

# table = soup.find('tbody')
# # print(table)

"""
'//*[@id="search-filter-results-3768"]/div[2]/div[5]/h3'
'//*[@id="search-filter-results-3768"]/div[2]/div[9]/h3'
'//*[@id="search-filter-results-3768"]/div[2]/div[13]/h3'
.
.
.
'//*[@id="search-filter-results-3768"]/div[2]/div[777]/h3'

'//*[@id="search-filter-results-3768"]/div[2]/div[6]'
.
.
.
'//*[@id="search-filter-results-3768"]/div[2]/div[774]'
'//*[@id="search-filter-results-3768"]/div[2]/div[778]'
"""
Company = []
Address = []
Sites = []
Phone = []
com = 1
det = 2

for _ in range(1, 195):

    com = com+4
    det = det+4
    company_name = driver.find_element(by=By.XPATH, value='//*[@id="search-filter-results-3768"]/div[2]/div[{}]'.format(com))
    company_name = company_name.text

    details_name = driver.find_element(by=By.XPATH, value='//*[@id="search-filter-results-3768"]/div[2]/div[{}]'.format(det))
    details = details_name.text.split("\n")
    print("*"*100)
    print("Row : ",details)
    print()

    if len(details) == 3:
        print("Company Name : ",company_name)
        Company.append(company_name)
        print("Address : ",details[0])
        Address.append(details[0])
        
        if ".com" in details[1] or ".org" in details[1] or ".net" in details[1]: 
            print("Site : ",details[1])
            Sites.append(details[1])
        else:
            Sites.append("")
        
        if any(chr.isdigit() for chr in details[1]):
            print("Phone : ",details[1])
            Phone.append(details[1])
        else:
            print("Phone : ",details[2])
            Phone.append(details[2])
    
    if len(details) == 2:
        print("Company Name : ",company_name)
        Company.append(company_name)
        print("Address : ",details[0])
        Address.append(details[0])
    
        if ".com" in details[1] or ".org" in details[1] or ".net" in details[1]: 
            print("Site : ",details[1])
            Sites.append(details[1])
        else:
            Sites.append("")
        
        if any(chr.isdigit() for chr in details[1]):
            print("Phone : ",details[1])
            Phone.append(details[1])
        else:
            Phone.append("")
        
        
        

dict1 = {
    "Company Name": Company,
    "Address": Address,
    "Site": Sites,
    "Phone": Phone
}

print("C : ",len(Company))
print("A : ",len(Address))
print("S : ",len(Sites))
print("P : ",len(Phone))

df = pd.DataFrame(dict1)
df.to_csv("riocertification.csv")

print(com)
print(det)