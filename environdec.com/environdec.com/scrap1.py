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

try:
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
    f = open('links.txt', 'r')
    links_to_scrap = f.read().split("\n")
    print(len(links_to_scrap))
    # sys.exit()
    
    reserve = ["Detailed information", "Registration number", "Status", "Registration date", "Valid until", "Geographical scopes", "Company information", "Company Name", "Country", "Contact", "Website"]
    seq = ["Registration number", "Status", "Registration date", "Version date :", "Valid until", "Geographical scopes", "Company Name", "Country", "Contact", "Website"]
    columns = ["Product Description", "Registration Number", "Status", "Registration Date", "Version Date",
            "Valid Until", "Geographical Scope", "Company Name", "Country Name", "Contact", "Website", "Pdf"
    ]

    f1 = open('link_error.txt', 'a')
    csv_writer = open("level_ecomedes.csv", "a")
    writer_obj = writer(csv_writer)
    driver= webdriver.Chrome(options=chrome_options, executable_path='/home/ritesh/Videos/WorkBook/Imogen&Jay/Scrapping/chromedriver')
    try:
        for index, link in enumerate(links_to_scrap[:10]):
            row = []
            # link = "https://www.environdec.com/library/epd1497"
            try:
                print("Length of scraps : ",len(links_to_scrap))
                print("-------------------------",index)
                print(link)
                if index % 5 == 0:
                    try:
                        driver.close()
                    except Exception as e:
                        print("Driver closing error : ",e)
                        # pass
                    time.sleep(2)
                    driver= webdriver.Chrome(options=chrome_options, executable_path='/home/ritesh/Videos/WorkBook/Imogen&Jay/Scrapping/chromedriver')
                
                driver.get(link)
                product_info = driver.find_elements_by_xpath('//*[@id="__next"]/main/div[2]')
                time.sleep(1)
                for j in product_info:
                    _d = "\n".join([i for i in j.text.split("\n")[1:]])
                    print("Product Information : ",_d)
                    product_description.append(_d)
                    row.append(_d)

                print("*"*50)
                detail_info = driver.find_elements_by_xpath('//*[@id="__next"]/main/div[3]')

                time.sleep(1)
                for k in detail_info:
                    print(k.text)
                    li = k.text.split("\n")
                    _info = []
                    li_name = []
                    print("."*100)

                    for index, i in enumerate(li):
                        if ":" in i:
                            if "https" not in i:
                                # print(i)
                                li_name.append(i)
                                if li[index+1].replace(":","") in seq:
                                    # print()
                                    _info.append("")
                                else:
                                    # print(li[index+1])
                                    _info.append(li[index+1])

                    print(":"*100)
                    print(seq)
                    # print(li_name)
                    print(_info)
                    # driver.close()
                    # sys.exit()
                    try:
                        if _info[0] not in reserve:
                            print("Registration Number : ",_info[0])
                            registration_number.append(_info[0])
                            row.append(_info[0])
                        else:
                            registration_number.append("")
                            row.append("")
                    except:
                        registration_number.append("")
                        row.append("")
                    try:
                        if _info[1] not in reserve:
                            print("Status : ",_info[1])
                            status.append(_info[1])
                            row.append(_info[1])
                        else:
                            status.append("")
                            row.append("")
                    except:
                        status.append("")
                        row.append("")
                    try:
                        if _info[2] not in reserve:
                            print("Registration date : ",_info[2])
                            registration_date.append(_info[2])
                            row.append(_info[2])
                        else:
                            registration_date.append("")
                            row.append("")
                    except:
                        registration_date.append("")
                        row.append("")
                    try:
                        if _info[3] not in reserve:
                            print("Version date : ",_info[3])
                            version_date.append(_info[3])
                            row.append(_info[3])
                        else:
                            version_date.append("")
                            row.append("")
                    except:
                        version_date.append("")
                        row.append("")
                    try:
                        if _info[4] not in reserve:
                            print("Valid until : ",_info[4])
                            valid_until.append(_info[4])
                            row.append(_info[4])
                        else:
                            valid_until.append("")
                            row.append("")
                    except:
                        valid_until.append("")
                        row.append("")
                    try:
                        if _info[5] not in reserve:
                            print("Geographical scopes : ",_info[5])
                            geo_scope.append(_info[5])
                            row.append(_info[5])
                        else:
                            geo_scope.append("")
                            row.append("")
                    except:
                        geo_scope.append("")
                        row.append("")
                    try:
                        if _info[6] not in reserve:
                            print("Company Name : ",_info[6])
                            company_name.append(_info[6])
                            row.append(_info[6])
                        else:
                            company_name.append("")
                            row.append("")
                    except:
                        company_name.append("")
                        row.append("")
                    try:
                        if _info[7] not in reserve:
                            print("Country : ",_info[7])
                            country_name.append(_info[7])
                            row.append(_info[7])
                        else:
                            country_name.append("")
                            row.append("")
                    except:
                        country_name.append("")   
                        row.append("")                 
                    try:
                        if _info[8] not in reserve:
                            print("Contact : ",_info[8])
                            contact.append(_info[8])
                            row.append(_info[8])
                        else:
                            contact.append("")
                            row.append("")
                    except:
                        contact.append("")
                        row.append("")
                    try:
                        if _info[9] not in reserve:
                            print("Website : ",_info[9])
                            website.append(_info[9])
                            row.append(_info[9])
                        else:
                            website.append("")
                            row.append("")
                    except:
                        website.append("")
                        row.append("")
                print("/"*100)

                download = driver.find_elements_by_xpath('//*[@id="__next"]/main/div[4]/div[1]/a')
                time.sleep(1)
                files = ""
                for index, x in enumerate(download):
                    if index > 0:
                        files += ", "
                    try:
                        print("Pdf Name : ",x.text)
                        link = x.get_attribute('href')
                        print("Pdf link : ",link)
                        files += str(link)
                        
                        # if 'pdf' in x.text:
                        #     wget.download(link, "Pdf/"+str(x.text))
                        # else:
                        #     wget.download(link, "Pdf/"+str(x.text)+".pdf")
                    except:
                        files = ""
                
                pdf_link.append(files)
                row.append(files)

                # print("Pdf link----------------")
                # print(pdf_link)
                
                print("Row-------------------")
                if len(columns) == len(row):
                    print(row)
                    writer_obj.writerow(row)
                else:
                    f1.write(link)
                # sys.exit()

            except Exception as e:
                print("Error while searching detail : ",e)
        csv_writer.close()
    except Exception as e:
        print("Error in extraction : ",e)
        
    # dict1 = {
    #     "Product Description": product_description,
    #     "Registration Number": registration_number,
    #     "Status": status,
    #     "Registration Date": registration_date,
    #     "Version Date": version_date,
    #     "Valid Until": valid_until,
    #     "Geographical Scope": geo_scope,
    #     "Company Name": company_name,
    #     "Country Name": country_name,
    #     "Contact": contact,
    #     "Website": website,
    #     "Pdf": pdf_link
    # }

    # f = open('data.json', 'w')
    # f.write()
    
    # df = pd.DataFrame(dict1)
    
    # print(df.head())
    # df.to_csv("level_ecomedes.csv")
    
    driver.close()
    
except Exception as e:
    print("Error :",e)
    
    # driver.close()