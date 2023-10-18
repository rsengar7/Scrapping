import collections
import json
import re
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import scrapy
import pandas as pd
import xmltodict
from scrapy.http import FormRequest
import datetime

class euipoSpider1(scrapy.Spider):
    name='euipo'
    allowed_domains = ['euipo.europa.eu']
    start_urls = ['https://euipo.europa.eu/copla/ctmsearch/json']
    start=2257500


    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',    
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://euipo.europa.eu',
    'Referer': 'https://euipo.europa.eu/eSearch/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
              }

    payload = "start="+str(start)+"&rows=100&searchMode=basic&criterion_1=ApplicationNumber&term_1=&operator_1=OR&condition_1=CONTAINS&criterion_2=MarkVerbalElementText&term_2=&operator_2=OR&condition_2=CONTAINS&criterion_3=OppositionIdentifier&term_3=&operator_3=OR&condition_3=CONTAINS&sortField=ApplicationNumber&sortOrder=asc"
    print('payload----',payload)
    
    

    def start_requests(self):
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for url in self.start_urls:
            # Uses the Scraper API service to get the source data. Scraper API is a service which uses proxy to bypass bot detection. 
            yield scrapy.Request(url,method='POST', callback=self.parseId,headers=self.headers,body=self.payload)           


    def parseId(self, response):
        
        json_data=json.loads(response.text)
        # print('data-----------------------------------------',json_data) 
        for item in json_data['items']:  
            li={}
            li['Filing Number']=item['numberToShow']
            yield li
        

        #move to next page
        self.start+=100
        if(self.start<json_data['total']):
            self.payload=re.sub(r'^start=[\d]+','start='+str(self.start),self.payload)
            print('Updated payload---------------------------------------',self.payload)
            url="https://euipo.europa.eu/copla/ctmsearch/json"
            yield scrapy.Request(url,method='POST', callback=self.parseId,headers=self.headers,body=self.payload)  
            


