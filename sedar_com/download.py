import time, sys, os, json
import wget
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from csv import writer
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from io import BytesIO
from PIL import Image

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

download_dir = "Pdf/"

settings = {
       "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# driver= webdriver.Chrome(options=chrome_options, executable_path='C:\\Users\\rseng\\Documents\\Imogen&Jay\\Scrapping\\chromedriver.exe')
li = []
counter = 0
try:
    for i in os.listdir('New'):
        print(i)
        li.append(i)

        df = pd.read_csv('New/'+i)

        urls = df['Docuement URL']

        

        for index, url in enumerate(urls):
            if index > 814:
                print("*"*50)
                print(index,"------",len(urls),"--------",url)
                print("*"*50)
                driver.get(url)

                time.sleep(3)


                if counter == 0:
                    time.sleep(40)
                elif index == 5:
                    pass
                    # sys.exit()
                else:
                    time.sleep(2)

                driver.execute_script('window.print();')

                time.sleep(3)
                counter+=1
        break

except Exception as e:
    pass

print()
print(li)
