import sys
import requests
import time
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import mysql.connector as mysqldb
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler


def db_conn():
    ''' DataBase Connection '''
    try:
        connection = mysqldb.connect(host="ls-16690a180e0a6fd4b048227253a3ef5e682b6253.cfxfiziytxdd.us-east-1.rds.amazonaws.com", port=3306, database="scrapper", user="dbmasteruser", password="hT(_ZaIBhop,fCrTJ?x=7#g?rX.Aw$lS", autocommit=True)
    except Exception as err:
        connection = mysqldb.connect(host="ls-16690a180e0a6fd4b048227253a3ef5e682b6253.cfxfiziytxdd.us-east-1.rds.amazonaws.com", port=3306, database="scrapper", user="dbmasteruser", password="hT(_ZaIBhop,fCrTJ?x=7#g?rX.Aw$lS", autocommit=True)
        print(err)
    return connection


def index():
    conn = db_conn()
    cur = conn.cursor()
    
    API_KEY = '4dad2ae3f844b433b12b87db830292c5'
    URL_TO_SCRAPE = 'https://www.globenewswire.com/'
    
    payload = {'api_key': API_KEY, 'url': URL_TO_SCRAPE}

    req = requests.get('http://api.scraperapi.com', params=payload, timeout=60)

    html = req.text.strip()
    soup = BeautifulSoup(html, 'lxml')

    company_title =[entry.text.lower() for entry in soup.find_all('p', {"class":'company-title'})]

    news = [entry.text.lower() for entry in soup.find_all('h1', {"class":'post-title16px'})]

    time = [entry.text.lower().split("ago")[0] + "ago" for entry in soup.find_all('p', {"class":'post-metadata'})]

    
    data = []
    for i in range(len(company_title)):
        data.append((company_title[i],news[i],time[i]))
    print(data)
    cur.execute("TRUNCATE TABLE dataset")
    if len(data) != 0:
        for x in data:
            print(x)
            cur.execute("""INSERT INTO dataset(company_title,news,timestamp) VALUES (%s, %s, %s)""", x)
        
        cur.close()
        conn.close()

    

# sched = BackgroundScheduler(daemon=True)
# sched.add_job(index,'interval', seconds=5, max_instances=2)
# sched.start()


application = Flask(__name__)
api = Api(application)

@application.route("/show")
def show():
    conn = db_conn()
    cur = conn.cursor()
    
    df = pd.read_sql_query("select company_title,news,timestamp from dataset", conn)
    data = df.values.tolist()

    print(df)
    print("Length------------",len(data))

    company_title = [i[0] for i in data]
    news = [i[1] for i in data]
    time = [i[2] for i in data]
    cur.close()
    conn.close()
    return jsonify({"data":{"company_title":company_title,"news":news,"timestamp":time}})


if __name__ == "__main__":
    application.run(host='0.0.0.0', port='8000')


