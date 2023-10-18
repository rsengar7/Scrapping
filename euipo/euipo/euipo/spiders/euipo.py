import collections
import json
import re
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import scrapy
import pandas as pd
# import xmltodict
from scrapy.http import FormRequest
import datetime
import csv

class euipoSpider2(scrapy.Spider):
    name='euipo'
    allowed_domains = ['euipo.europa.eu']
    

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://euipo.europa.eu/eSearch/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    
    def start_requests(self):
        with open(r'C:\Users\sysadmin\Documents\Python Scripts\euipo\id_6.csv') as file_obj:
            items = csv.reader(file_obj)
            next(items)
            for row in items:  
                print('row-------------------',row)
                item_url='https://euipo.europa.eu/copla//trademark/data/withOppoRelations/'+''.join(row)
                yield scrapy.Request(item_url,method='GET', callback=self.parseItem,headers=self.headers)



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
