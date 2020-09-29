from selenium import webdriver
import time
import datetime

driver= webdriver.Chrome(executable_path="/home/ritesh/Videos/Jason/Scrapper/chromedriver")
while True:
    li = ["https://www.openmarket.com/docs/Content/releasenotes/benefits.htm", "https://mms-reporting.openmarket.com/messageReport?0", "https://www.openmarket.com/docs/Content/sms.htm", "https://www.openmarket.com/docs/Content/apis/sms/sms-get-started.htm", "https://www.openmarket.com/docs/Content/apis/v4http/things-to-know.htm#Messagerequest", "https://www.openmarket.com/docs/Content/apis/v4http/send-json.htm"]
    for i in li:
        driver.get(i)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # driver.find_element_by_xpath("(//input[@type='text'])[2]").click()
        # driver.find_element_by_xpath("(//input[@type='text'])[2]").clear()
        # driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(location)
        # driver.find_element_by_xpath("//button[@type='submit']").click()
        # time.sleep(4)
        # driver.find_element_by_xpath("//div[@id='weather-widget']/div/div/div/div[2]/div/div/ul/li").click()
        # time.sleep(4)
        # data = driver.find_element_by_xpath("//div[@id='weather-widget']/div[2]/div/div/div[2]/div/span").text

        # print("Temperature of '{}' at '{}' -->> '{}'".format(location, datetime.datetime.now(), data))
        # print()
        time.sleep(300)