import time, sys
import wget
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')



driver= webdriver.Chrome(options=chrome_options, executable_path='/home/ritesh/Videos/WorkBook/Imogen&Jay/Scrapping/chromedriver')

try:
    driver.get("https://www.environdec.com/library")
    time.sleep(4)
    
    driver.execute_script("window.scrollTo(0, 800);")
    
    
    for _ in range(1, 200):
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(5)
    
    product_description = []
    registration_number = []
    status = []
    registration_date = []
    version_date = []
    valid_until = []
    geo_scope = []
    company_name = []
    country_name = []
    contact = []
    website = []
    pdf_link = []
    
    links_to_scrap = []
    
    for index in range(1, 3016):
        print()
        print()
        print()
        print("Index ------>",index)
        print('//*[@id="__next"]/main/div[1]/a[{}]'.format(index))

        data = driver.find_elements_by_xpath('//*[@id="__next"]/main/div[1]/a[{}]'.format(index))
        print(data)
        
        for i in data:
            link = i.get_attribute('href')
            print("Link : ",link)
            links_to_scrap.append(link)
        
    print("length ---->", len(links_to_scrap))
    f = open('links.txt', 'w')
    for i in links_to_scrap:
        f.write(i)
        f.write("\n")
    f.close()
    sys.exit()
    
    try:
        for index, link in enumerate(links_to_scrap):
            try:
                print("Length of scraps : ",len(links_to_scrap))
                print("-------------------------",index)
                print(link)
                driver.get(link)
                product_info = driver.find_elements_by_xpath('//*[@id="__next"]/main/div[2]')
                time.sleep(1)
                for j in product_info:
                    print("Product Information : ",j.text.split("\n")[1])
                    product_description.append(j.text.split("\n")[1])

                print("*"*50)
                detail_info = driver.find_elements_by_xpath('//*[@id="__next"]/main/div[3]')

                time.sleep(1)
                for k in detail_info:
                    print(k.text)
                    _info = k.text.split("\n")
                    print(":"*100)
                    try:
                        print("Registration Number : ",_info[2])
                        registration_number.append(_info[2])
                    except:
                        registration_number.append("")
                    try:
                        print("Status : ",_info[4])
                        status.append(_info[4])
                    except:
                        status.append("")
                    try:
                        print("Registration date : ",_info[6])
                        registration_date.append(_info[6])
                    except:
                        registration_date.append("")
                    try:
                        print("Version date : ",_info[8])
                        version_date.append(_info[8])
                    except:
                        version_date.append("")
                    try:
                        print("Valid until : ",_info[10])
                        valid_until.append(_info[10])
                    except:
                        valid_until.append("")
                    try:
                        print("Geographical scopes : ",_info[12])
                        geo_scope.append(_info[12])
                    except:
                        geo_scope.append("")
                    try:
                        print("Company Name : ",_info[15])
                        company_name.append(_info[15])
                    except:
                        company_name.append("")
                    try:
                        print("Country : ",_info[17])
                        country_name.append(_info[17])
                    except:
                        country_name.append("")
                    try:
                        print("Contact : ",_info[19])
                        contact.append(_info[19])
                    except:
                        contact.append("")
                    try:
                        print("Website : ",_info[21])
                        website.append(_info[21])
                    except:
                        website.append("")
                print("/"*100)

                download = driver.find_elements_by_xpath('//*[@id="__next"]/main/div[4]/div[1]/a')
                time.sleep(1)
                for x in download:
                    try:
                        print("Pdf Name : ",x.text)
                        link = x.get_attribute('href')
                        print("Pdf link : ",link)
                        pdf_link.append(link)
                        if 'pdf' in x.text:
                            wget.download(link, "Pdf/"+str(x.text))
                        else:
                            wget.download(link, "Pdf/"+str(x.text)+".pdf")
                    except:
                        pdf_line.append("")
            except Exception as e:
                print("Error while searching detail : ",e)
    except Exception as e:
        print("Error in extraction : ",e)
        
    dict1 = {
        "Product Description": product_description,
        "Registration Number": registration_number,
        "Status": status,
        "Registration Date": registration_date,
        "Version Date": version_date,
        "Valid Until": valid_until,
        "Geographical Scope": geo_scope,
        "Company Name": company_name,
        "Country Name": country_name,
        "Contact": contact,
        "Website": website,
        "Pdf": pdf_link
    }
    
    df = pd.DataFrame(dict1)
    
    print(df.head())
    df.to_csv("level_ecomedes.csv")
    
    driver.close()
    
except Exception as e:
    print("Error :",e)
    
    driver.close()