from selenium import webdriver
import time
import datetime

location = input("Enter the Location Name : ")

driver= webdriver.Chrome(executable_path="/home/ritesh/Videos/Jason/Scrapper/chromedriver")

while True:
    driver.get("https://openweathermap.org/")
    time.sleep(3)
    driver.find_element_by_xpath("(//input[@type='text'])[2]").click()
    driver.find_element_by_xpath("(//input[@type='text'])[2]").clear()
    driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(location)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(4)
    driver.find_element_by_xpath("//div[@id='weather-widget']/div/div/div/div[2]/div/div/ul/li").click()
    time.sleep(4)
    data = driver.find_element_by_xpath("//div[@id='weather-widget']/div[2]/div/div/div[2]/div/span").text

    print("Temperature of '{}' at '{}' -->> '{}'".format(location, datetime.datetime.now(), data))
    print()
    # time.sleep(289)