import collections
import json
import re
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import scrapy
import pandas as pd
import xmltodict
from scrapy.http import FormRequest
import datetime

class euipoSpider(scrapy.Spider):
    name='euipo'
    allowed_domains = ['euipo.europa.eu']
    start_urls = ['https://euipo.europa.eu/copla/ctmsearch/json']
    start=0


    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',    
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://euipo.europa.eu',
    'Referer': 'https://euipo.europa.eu/eSearch/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
              }

    payload = "start=0&rows=100&searchMode=basic&criterion_1=ApplicationNumber&term_1=&operator_1=OR&condition_1=CONTAINS&criterion_2=MarkVerbalElementText&term_2=&operator_2=OR&condition_2=CONTAINS&criterion_3=OppositionIdentifier&term_3=&operator_3=OR&condition_3=CONTAINS&sortField=ApplicationNumber&sortOrder=asc"
    
    
    
    

    def start_requests(self):

        
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for url in self.start_urls:
            # Uses the Scraper API service to get the source data. Scraper API is a service which uses proxy to bypass bot detection. 
            yield scrapy.Request(url,method='POST', callback=self.parseTrademarks,headers=self.headers,body=self.payload)           


    def parseTrademarks(self, response):
        
        json_data=json.loads(response.text)
        #print('data-----------------------------------------',json_data) 
         
        for item in json_data['items']:
          item_url='https://euipo.europa.eu/copla//trademark/data/withOppoRelations/'+item['numberToShow']  
          yield scrapy.Request(item_url,method='GET', callback=self.parseItem,headers=self.headers)
        

        #move to next page
        self.start+=100
        if(self.start<json_data['total']):
            self.payload=re.sub(r'^start=[\d]+','start='+str(self.start),self.payload)
            print('Updated payload---------------------------------------',self.payload)
            url="https://euipo.europa.eu/copla/ctmsearch/json"
            yield scrapy.Request(url,method='POST', callback=self.parseTrademarks,headers=self.headers,body=self.payload)  
            




    def parseItem(self, response): 
         
        json_data=json.loads(response.text)
        

        li={}
        
        li['url']=response.url
          
        try:
            li['Name']=json_data['entity']['name']
        except:
            li['Name']=''

        try:
            li['Filing number']=json_data['entity']['number']
        except:
            li['Filing number']=''

        try:
            li['Basis']=json_data['entity']['basis']
        except:
            li['Basis']=''

        try:
            li['Filing language']=json_data['entity']['firstlang']
        except:
            li['Filing language']==''

        try:
            li['Type']=json_data['entity']['feature']
        except:
            li['Type']=''

        try:
            li['Nature']=json_data['entity']['kind']
        except:  
            li['Nature']=''

        try:
            li['Nice Class']=','.join(json_data['entity']['niceclasses']) 
        except:
            li['Nice Class']=''

        try:
            li['Vienna Classification']=','.join(json_data['entity']['viennaclassification'])
        except:
            li['Vienna Classification']=''

        try:
            li['Second language']=json_data['entity']['secondlang']
        except:
           li['Second language']='' 

        try:
            li['Reference']=json_data['entity']['reference']
        except:
            li['Reference']=''

        try:
            li['Trade mark status']=json_data['entity']['status']
        except:
            li['Trade mark status']=''

        try:
            li['Acquired distinctiveness']=json_data['entity']['distinctiveness']
        except:
            li['Acquired distinctiveness']=''

        try:
            ts=int(str(json_data['entity']['filingdate'])[:-3])
            filingdate=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            li['Filing Date']=filingdate
        except:
            li['Filing Date']=''

        try:
            ts=int(str(json_data['entity']['regdate'])[:-3])
            regdate=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            li['Registered Date']=regdate
        except:
            li['Registered Date']=''

        try:
            ts=int(str(json_data['entity']['expirydate'])[:-3])
            expirydate=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            li['Expiry Date']=expirydate
        except:
            li['Expiry Date']=''

        try:
            ts=int(str(json_data['entity']['receivedate'])[:-3])
            receivedate=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            li['Date of receipt']=receivedate
        except:
            li['Date of receipt']=''

        try:
            ts=int(str(json_data['entity']['currentStatusDate'])[:-3])
            currentStatusDate=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            li['Current Status Date']=currentStatusDate
        except:
            li['Current Status Date']=''

        try:
            ts=int(str(json_data['entity']['designationdate'])[:-3])
            designationdate=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            li['Designation Date']=designationdate
        except:
             li['Designation Date']=''

        yield li