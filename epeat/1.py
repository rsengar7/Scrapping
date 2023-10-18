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

driver.get()