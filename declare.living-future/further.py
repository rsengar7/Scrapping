declare_id = '//*[@id="root"]/div/div/div/div[2]/div/div[2]/div[1]/span'
licence_expiration = '//*[@id="root"]/div/div/div/div[2]/div/div[2]/div[2]/span'

'//*[@id="root"]/div/div/div/div[2]/div/div[2]/div[1]'

import time, sys, os
import wget
import pandas as pd
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

df = pd.read_csv('declare-living.csv')

# urls = df['URL'].values.tolist()
data = df.values.tolist()

# print(data)

# sys.exit()

Declare_id = []
Licence_expiration = []
Lpc_certified = []
Life_expectancy = []
End_of_life_options = []
Declared_unit = []
Embodied_carbon = []
Assessor = []
Phone = []
Ingredient_list = []
Urls_list = []
Companys = []
Products = []

error_url = []

for row in data:
    print(row)
    url = row[1]
    product = row[2]
    company = row[3]
    try:

        driver.get(url)

        # driver.get('https://declare.living-future.org/products/adapt-46')
        # # driver.get('https://declare.living-future.org/products/apa-asl-accent-cube-quietspace-panel')

        product_name = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div/div[2]/div/div[2]')

        declare_id = ""
        licence_expiration = ""
        lpc_certified = ""
        life_expectancy = ""
        end_of_life_options = ""
        declared_unit = ""
        embodied_carbon = ""
        assessor = ""
        phone = ""

        for row in product_name.text.split('\n'):
            if len(row.split('DECLARE ID')) > 1:
                declare_id = row.split('DECLARE ID')[1]
            elif len(row.split('LICENSE EXPIRATION')) > 1:
                licence_expiration = row.split('LICENSE EXPIRATION')[1]
            elif len(row.split('LIVING PRODUCT CHALLENGE (LPC) CERTIFIED')) > 1:
                lpc_certified = row.split('LIVING PRODUCT CHALLENGE (LPC) CERTIFIED')[1]
            elif len(row.split('LIFE EXPECTANCY')) > 1:
                life_expectancy = row.split('LIFE EXPECTANCY')[1]
            elif len(row.split('END OF LIFE OPTIONS')) > 1:
                end_of_life_options = row.split('END OF LIFE OPTIONS')[1]
            elif len(row.split('DECLARED UNIT')) > 1:
                declared_unit = row.split('DECLARED UNIT')[1]
            elif len(row.split('EMBODIED CARBON')) > 1:
                embodied_carbon = row.split('EMBODIED CARBON')[1]
            elif len(row.split('ASSESSOR')) > 1:
                assessor = row.split('ASSESSOR')[1]
            else:
                pass
            
        product_name = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div/div[2]/div/div[4]')
        for row in product_name.text.split("\n"):
            if len(row.split(":")) > 1:
                phone = row.split(":")[1]
            
        product_name = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div/div[2]/div/div[3]')

        Ingredient_name = []
        Cas = []
        Percentage = []
        dict1 = []

        for index, row in enumerate(product_name.text.split('\n')):
            if index > 1:
                row = row.replace("< ", "<").replace("> ", ">")
                if len(row.split(" ")) == 4:
                    # print("Ingredient Name 4: ",row.split(" ")[:2], "---- CAS# : ",row.split(" ")[2], "----- Percentage :",row.split(" ")[3])
                    Ingredient_name.append(" ".join(row.split(" ")[:2]))
                    Cas.append(row.split(" ")[2])
                    Percentage.append(row.split(" ")[3])

                    dict1.append({
                        "Ingredient_name": " ".join(row.split(" ")[:2]),
                        "Cas#": row.split(" ")[2],
                        "Percentage": row.split(" ")[3]
                    })
                elif len(row.split(" ")) == 5:
                    # print("Ingredient Name 5: ",row.split(" ")[:3], "---- CAS# : ",row.split(" ")[3], "----- Percentage :",row.split(" ")[4])
                    Ingredient_name.append(" ".join(row.split(" ")[:3]))
                    Cas.append(row.split(" ")[3])
                    Percentage.append(row.split(" ")[4])

                    dict1.append({
                        "Ingredient_name": " ".join(row.split(" ")[:3]),
                        "Cas#": row.split(" ")[3],
                        "Percentage": row.split(" ")[4]
                    })

                elif len(row.split(" ")) == 6:
                    # print("Ingredient Name 6: ",row.split(" ")[:4], "---- CAS# : ",row.split(" ")[4], "----- Percentage :",row.split(" ")[5])
                    Ingredient_name.append(" ".join(row.split(" ")[:4]))
                    Cas.append(row.split(" ")[4])
                    Percentage.append(row.split(" ")[5])

                    dict1.append({
                        "Ingredient_name": " ".join(row.split(" ")[:4]),
                        "Cas#": row.split(" ")[4],
                        "Percentage": row.split(" ")[5]
                    })

                elif len(row.split(" ")) == 7:
                    # print("Ingredient Name 7: ",row.split(" ")[:5], "---- CAS# : ",row.split(" ")[5], "----- Percentage :",row.split(" ")[6])
                    Ingredient_name.append(" ".join(row.split(" ")[:5]))
                    Cas.append(row.split(" ")[5])
                    Percentage.append(row.split(" ")[6])

                    dict1.append({
                        "Ingredient_name": " ".join(row.split(" ")[:5]),
                        "Cas#": row.split(" ")[5],
                        "Percentage": row.split(" ")[6]
                    })

                elif len(row.split(" ")) == 8:
                    # print("Ingredient Name 8: ",row.split(" ")[:6], "---- CAS# : ",row.split(" ")[6], "----- Percentage :",row.split(" ")[7])
                    Ingredient_name.append(" ".join(row.split(" ")[:6]))
                    Cas.append(row.split(" ")[6])
                    Percentage.append(row.split(" ")[7])

                    dict1.append({
                        "Ingredient_name": " ".join(row.split(" ")[:6]),
                        "Cas#": row.split(" ")[6],
                        "Percentage": row.split(" ")[7]
                    })

                elif len(row.split(" ")) == 9:
                    # print("Ingredient Name 9: ",row.split(" ")[:7], "---- CAS# : ",row.split(" ")[7], "----- Percentage :",row.split(" ")[8])
                    Ingredient_name.append(" ".join(row.split(" ")[:7]))
                    Cas.append(row.split(" ")[7])
                    Percentage.append(row.split(" ")[8])

                    dict1.append({
                        "Ingredient_name": " ".join(row.split(" ")[:7]),
                        "Cas#": row.split(" ")[7],
                        "Percentage": row.split(" ")[8]
                    })

                elif len(row.split(" ")) == 10:
                    # print("Ingredient Name 10: ",row.split(" ")[:8], "---- CAS# : ",row.split(" ")[8], "----- Percentage :",row.split(" ")[9])
                    Ingredient_name.append(" ".join(row.split(" ")[:8]))
                    Cas.append(row.split(" ")[8])
                    Percentage.append(row.split(" ")[9])

                    dict1.append({
                        "Ingredient_name": " ".join(row.split(" ")[:8]),
                        "Cas#": row.split(" ")[8],
                        "Percentage": row.split(" ")[9]
                    })

                else:
                    # print("Ingredient Name 3: ",row.split(" ")[0], "---- CAS# : ",row.split(" ")[1], "----- Percentage :",row.split(" ")[2])
                    Ingredient_name.append(row.split(" ")[0])
                    Cas.append(row.split(" ")[1])
                    Percentage.append(row.split(" ")[2])

                    dict1.append({
                        "Ingredient_name": " ".join(row.split(" ")[0]),
                        "Cas#": row.split(" ")[1],
                        "Percentage": row.split(" ")[2]
                    })

        # print("Ingredient Name : ",Ingredient_name)
        # print("Cas# : ",Cas)
        # print("Percentage : ",Percentage)


        print("declare_id : ",declare_id)
        # print("licence_expiration : ",licence_expiration)
        # print("lpc_certified : ",lpc_certified)
        # print("life_expectancy : ",life_expectancy)
        # print("end_of_life_options : ",end_of_life_options)
        # print("declared_unit : ",declared_unit)
        # print("embodied_carbon : ",embodied_carbon)
        # print("assessor : ",assessor)
        # print("Phone : ",phone)
        # print("INGREDIENT LIST : ",dict1)

        Declare_id.append(declare_id)
        Licence_expiration.append(licence_expiration)
        Lpc_certified.append(lpc_certified)
        Life_expectancy.append(life_expectancy)
        End_of_life_options.append(end_of_life_options)
        Declared_unit.append(declared_unit)
        Embodied_carbon.append(embodied_carbon)
        Assessor.append(assessor)
        Phone.append(phone)
        Ingredient_list.append(dict1)
        Urls_list.append(url)
        Companys.append(company)
        Products.append(product)

    except Exception as e:
        print("Error : ",e)
        error_url.append(url)

dict2 = {
    "Urls": Urls_list,
    "Company": Companys,
    "Product": Products,
    "Declare Id": Declare_id,
    "Licence Expiration": Licence_expiration,
    "Lpc Certified": Lpc_certified,
    "Life Expectancy": Life_expectancy,
    "End Of Life Options": End_of_life_options,
    "Declared Unit": Declared_unit,
    "Embodied Carbon": Embodied_carbon,
    "Assessor": Assessor,
    "Phone": Phone,
    "Ingredient List": Ingredient_list
}

df = pd.DataFrame(dict2)

df.to_csv('declare-living-detail.csv')

print("*"*100)
print(error_url)
print("*"*100)