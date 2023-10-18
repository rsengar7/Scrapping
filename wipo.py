"""
Source: https://branddb.wipo.int
"""

import collections
import json
import re
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import scrapy
import pandas as pd
import xmltodict
from scrapy.http import FormRequest

class wipoSpider(scrapy.Spider):
    name='wipo'
    allowed_domains = ['branddb.wipo.int']
    start_urls = ['https://api.branddb.wipo.int/explore?fg=_void_&rows=45&sort=applicationDate%20desc&start=0']
    brands=[]
    
    headers = {
                     'accept': 'application/json, text/plain, */*',
                     'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJ6aXAiOiJOT05FIiwia2lkIjoibGhXcVRBZklFa29kQm8yblVHaTNsaUZKRzFVPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJTSFJJTklESElHT1dEQSIsImN0cyI6Ik9BVVRIMl9TVEFURUxFU1NfR1JBTlQiLCJhdXRoX2xldmVsIjoxLCJhdWRpdFRyYWNraW5nSWQiOiJjYTFmYTY3NS04MTcxLTQxODYtODJjMC0zMWJiMDY3MGVlMWItMTMzNDg1MzEiLCJpc3MiOiJodHRwczovL3d3dzMud2lwby5pbnQvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiYzRYX2xLQW9obV9VamprZ1pFYVBHTXBndW9jIiwibm9uY2UiOiJRMmwxZFVFM2RFdEtSbTlwZW10a1JFOVBZVEZoVVVOYVVFeHBMVWRUVW1SM09YSjFNVFJCZW1OMWJGWlMiLCJhdWQiOiJvaWRjR0JEIiwibmJmIjoxNjY4NjE3NzIyLCJncmFudF90eXBlIjoidG9rZW4iLCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNjY4NjE3NzIyLCJyZWFsbSI6Ii8iLCJleHAiOjE2Njg2MjEzMjIsImlhdCI6MTY2ODYxNzcyMiwiZXhwaXJlc19pbiI6MzYwMCwianRpIjoiOXBXWGphQ0E5Z0NvS0lsSU9TYVZjdHZtUVU0In0.F4AWY7E66LRdON9OJaegexc0sCPvl04XB1rinwYn5FHqCn7XitvBvISzbCjAqojUORHdFEW_s78HBiHuMtj89cNc85P0gm1FkqR7qFMRh_irirIiGPmfAbI_yh9GHLLOKlSZgmI7vZdAqbrGUGpOUV6OeJBDRWYSRMDXy-89Q3aX9QBdG5ITVm_fsuADA8rE9XEhGryCaYCtPtsenDl9LFb0mDcjJjA6cy7ml93Tz6kyQ-D9N_38qPJWZMwDaoOHOum06aR91UZ-Pc-6x--CmEqDRGT7pnF3DE16EJQqwh_6dXDFkIGIGLd6mHAi8pzoAOtksfwpDK1bh1Fldj5owQ'
                    }

    def start_requests(self):
      
        
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for url in self.start_urls:
            # Uses the Scraper API service to get the source data. Scraper API is a service which uses proxy to bypass bot detection. 
            yield scrapy.Request(url,method='GET', callback=self.parse,headers=self.headers) 


    def parse(self, response):
        json_data=json.loads(response.text)
        #print(json_data['response']['docs'])  

        for item in json_data['response']['docs']:
            li={}

            li['URL']=response.url
            try:
                li['Brand']=','.join(item['brandName'])
            except:
                li['Brand']=''   
            try:
                li['Owner']=','.join(item['applicant'])
            except:
                li['Owner']=''
            
            try:
                li['Registration Number']=item['registrationNumber']
            except:
                li['Registration Number']='' 
            try:
                li['Application Number']=item['applicationNumber']
            except:
                li['Application Number']=''     
            try:
                li['Application Date']=item['applicationDate']
            except:
                li['Application Date']=''     
            try:
                li['Registration Date']=item['registrationDate']
            except:
                li['Registration Date']=''     
            try:
                li['Expiry Date']=item['expiryDate']
            except:
                li['Expiry Date']=''     
            try:
                li['Nice Class']=','.join([str(i) for i in item['niceClass']])                                      
            except:
                li['Nice Class']='' 
            try:
                li['Status']=item['status']
            except:
                li['Status']=''     
            try:
                li['Designation']=','.join(item['designation'])
            except:
                li['Designation']=''     
            try:
                li['Country Code']=','.join(item['applicantCountryCode'])
            except:
                li['Country Code']=''     
            try:
                li['IPR']=item['type']
            except:
                li['IPR']=''     
            try:
                li['Kind Of Mark']=','.join(item['kind'])
            except:
                li['Kind Of Mark']=''     
            try:
                li['Type Of Mark']=item['markFeature']
            except:
                li['Type Of Mark']=''     
            #self.brands.append(li)

            yield li


        
        
       
        start=json_data['response']['start']
        start+=45
        if(start<json_data['response']['numFound']):
            url=re.sub(r'\d+$',str(start),response.url)
            #print('url---------',url)
            yield scrapy.Request(url,method='GET', callback=self.parse,headers=self.headers)


    # def closed(self, reason):
    #         # will be called when the crawler process ends
    #         # any code 
    #         # do something with collected data 
    #     df = pd.DataFrame(self.brands)
    #     print(df)
    #     df.to_csv(self.name+'.csv',index=False)              
                  

        
    


    