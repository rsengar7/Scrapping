from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pynput.keyboard import Key,Controller
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, render_template, request
import os
import re
import requests

app = Flask(__name__)

def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    print(sentiment_dict,"-----",sentence)
    print("======================")
    if sentiment_dict['compound'] >= 0.05 :
        return "The Review Sentiment is Positive"
    elif sentiment_dict['compound'] <= - 0.05 :
        return "The Review Sentiment is Negative"
    else :
        return "The Review Sentiment is Neutral"

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':

        result = request.form['usrname']

        driver=webdriver.Chrome("C:\\Users\\Ritesh\\PycharmProjects\\MyPro\\drivers\\"
                                      "\\chromedriver.exe")

        input_url= result
        driver.get(input_url)
        # print("Product Link  :  "+input_url)
        time.sleep(2)

        html=driver.page_source
        soup=BeautifulSoup(html,features="lxml")
        data = soup.find("div", id="cm-cr-dp-review-list")
        usernames,ratings,reviews,sentiments = [],[],[],[]
        for text in data:
            username = text.find('span',class_="a-profile-name")
            usernames.append(str(username).replace("<",">").split(">")[2])

            rating = text.find('span', class_="a-icon-alt")
            ratings.append(str(rating).replace("<",">").split(">")[2])

            review = text.find('div', class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content")
            reviews.append(str(review).replace("<",">").split(">")[4])
            sentiments.append(sentiment_scores(str(review).replace("<",">").split(">")[4]))

        totaldata = []
        for index in range(len(usernames)):
            dict = {}
            dict['User'] = usernames[index]
            dict['Rating'] = ratings[index]
            dict['Review'] = reviews[index]
            dict['Review Sentiment'] = sentiments[index]
            totaldata.append(dict)
        print(totaldata)


        return render_template("index.html",totaldata = totaldata)

if __name__=='__main__':
    app.run(debug=True)

