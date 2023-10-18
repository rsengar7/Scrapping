import time, sys
import wget
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from csv import writer

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver= webdriver.Chrome(options=chrome_options, executable_path='/home/ritesh/Videos/WorkBook/Imogen&Jay/Scrapping/chromedriver')

driver.get("https://geca.eco/our-licensees/")

licenceUrl = {}
for index in range(1, 105):
    # //*[@id="myTable"]/tbody/tr[1]/td[3]/a
    # //*[@id="myTable"]/tbody/tr[2]/td[3]/a
    _data = driver.find_elements_by_xpath('//*[@id="myTable"]/tbody/tr[{}]/td[3]/a'.format(index))

    for i in _data:
        licenceUrl[i.get_attribute('href')] = i.text
    # break

# sys.exit()

# licenceUrl['https://geca.eco/licensees/abco-products/'] = 12
urls = []
websites = []
emails = []
numbers = []
standards = []
licences = []
availabilities = []
distributions = []
product_names = []
licneceNames = []
licenceNameUrls = []
gecaStandardName = []
gecaStandardNameUrl = []
pdf = []



for url, num in licenceUrl.items():
    print(url,"-----",num)


    driver.get(url)
    website = driver.find_elements_by_xpath('/html/body/section[2]/div/div[1]/div[1]/div[2]/ul/li[1]/div[2]/a')
    email = driver.find_elements_by_xpath('/html/body/section[2]/div/div[1]/div[1]/div[2]/ul/li[2]/div[2]/a[1]')
    number = driver.find_elements_by_xpath('/html/body/section[2]/div/div[1]/div[1]/div[2]/ul/li[2]/div[2]/a[2]')
    standard = driver.find_elements_by_xpath('/html/body/section[2]/div/div[1]/div[1]/div[2]/ul/li[3]/div[2]/h6')
    licence = driver.find_elements_by_xpath('/html/body/section[2]/div/div[1]/div[1]/div[2]/ul/li[4]/div[2]/h6')
    availability = driver.find_elements_by_xpath('/html/body/section[2]/div/div[1]/div[1]/div[2]/ul/li[5]/div[2]/div')
    distribution = driver.find_elements_by_xpath('/html/body/section[2]/div/div[1]/div[1]/div[2]/ul/li[6]/div[2]/div/h6')

    try:
        _website = website[0].text
    except:
        _website = ""
    print(_website)
    try:
        _email = email[0].text
    except:
        _email = ""
    print(_email)
    try:
        _number = number[0].text
    except:
        _number = ""
    print(_number)
    try:
        _standard = standard[0].text
    except:
        _standard = ""
    print(_standard)
    try:
        _licence = licence[0].text
    except:
        _licence
    print(_licence)
    try:
        _availability = availability[0].text
    except:
        _availability = ""
    print(_availability)
    try:
        _distribution = distribution[0].text
    except:
        _distribution = ""
    print(_distribution)
    
    # websites.append(website[0].text)
    # emails.append(email[0].text)
    # numbers.append(number[0].text)
    # standards.append(standard[0].text)
    # licences.append(licence[0].text)
    # availabilities.append(availability[0].text)
    # distributions.append(distribution[0].text)
    
    print("*"*100)
    temp_url = []
    for i in range(1, int(num)+1):
        print("Num ------>",num)
        print("Index----->",i)
        
        urls.append(url)
        time.sleep(1)

        _d = driver.find_elements_by_xpath('//*[@id="myTable"]/tbody/tr[{}]/td[2]/a'.format(i))
        try:
            print(_d)
            print(_d[0])
            print(_d[0].text)
            product_names.append(_d[0].text)
        except:
            product_names.append("")
        try:
            link = _d[0].get_attribute('href')
            print(link)
            temp_url.append(link)
        except:
            pass

    for links in temp_url:
        driver.get(link)

        licenceName = driver.find_elements_by_xpath('/html/body/section[2]/div/div[2]/div[1]/div/ul/li[1]/div[2]/h6/a')
        try:
            licneceNames.append(licenceName[0].text)
        except:
            licneceNames.append("")
        try:
            licenceNameUrls.append(licenceName[0].get_attribute('href'))
        except:
            licenceNameUrls.append("")

        gecastandard = driver.find_elements_by_xpath('/html/body/section[2]/div/div[2]/div[1]/div/ul/li[3]/div[2]/h6/a')
        try:
            gecaStandardName.append(gecastandard[0].text)
        except:
            gecaStandardName.append("")
        try:
            gecaStandardNameUrl.append(gecastandard[0].get_attribute('href'))
        except:
            gecaStandardNameUrl.append("")

        files = driver.find_elements_by_xpath('/html/body/section[2]/div/div[2]/div[1]/div/ul/li[5]/div[1]/div[2]/p/a')
        try:
            pdf.append(files[0].get_attribute('href'))
        except:
            pdf.append("")

        websites.append(_website)
        emails.append(_email)
        numbers.append(_number)
        standards.append(_standard)
        licences.append(_licence)
        availabilities.append(_availability)
        distributions.append(_distribution)




    # //*[@id="myTable"]/tbody/tr[1]/td[2]/a
    # //*[@id="myTable"]/tbody/tr[2]/td[2]/a

dict1 = {
'urls': urls,
'websites': websites,
'emails': emails,
'numbers': numbers,
'standards': standards,
'licences': licences,
'availabilities': availabilities,
'distributions': distributions,
'product_names': product_names,
'licneceNames': licneceNames,
'licenceNameUrls': licenceNameUrls,
'gecaStandardName': gecaStandardName,
'gecaStandardNameUrl': gecaStandardNameUrl,
'pdf': pdf
}

print(dict1)

df = pd.DataFrame(dict1)

print(df.head())

df.to_csv('geca_eco.csv')

driver.close()