import re
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import scrapy
import pandas as pd
import xmltodict
import json
import datetime

class openLCANexusSpider(scrapy.Spider):
    name='openLCANexus'
    allowed_domains = ['nexus.openlca.org']
    start_urls = ['https://nexus.openlca.org/ws/search/datasets']
    datasets=[]
    
    def start_requests(self):
        headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.9'
                  }
      
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for url in self.start_urls:
            # Uses the Scraper API service to get the source data. Scraper API is a service which uses proxy to bypass bot detection. 
            yield scrapy.Request(url,method='GET', callback=self.parseCategories,headers=headers)

    def parseCategories(self, response):
        headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.9'
                  }
        json_data=json.loads(response.text)
        #print(json_data['aggregations'])
        for item in json_data['aggregations']:
            if(item['name'] == 'categoryPath'):
                for processcat in item['entries']:
                    if('/' not in processcat['key']):  
                      #if(processcat['key']=='Seeds'):
                        # print('process cat ------------------------------------->',processcat['key'])  
                        # print('Cat count------------------------------------->',catcount)
                        url='https://nexus.openlca.org/ws/search/datasets?categoryPath='+processcat['key']
                        yield scrapy.Request(url,method='GET', callback=self.parseItem,headers=headers)
                        
                     
       

    def parseItem(self, response):
        #self.pageCount+=1
        #print("current page is ------> ",self.pageCount)
        json_data=json.loads(response.text)
        #print(json_data)

        for item in json_data['data']:
            li={}
            try:
                li['URL']='https://nexus.openlca.org/search/'+response.request.url.split('?')[1].replace('&','!')
            except:
                pass    

            try:
                li['Name']=item['name']
            except:
                li['Name']=''   
            try:    
                li['Category']=item['category']
            except:
                li['Category']=''       
            try:
                li['Databases']=','.join(item['databases'])
            except:
                li['Databases']='' 
            try:  
                li['System Model']=','.join(item['systemModel']).replace('_',' ')
            except:
                li['System Model']=''
            try:       
                li['Location']=item['location']
            except:
                li['Location']=''   
            try:
                li['Validity']=str(item['validFromYear'])+'-'+str(item['validUntilYear'])
            except:
                li['Validity']='' 
            try:   
                li['Description']=item['description'].strip()
            except:
                li['Description']='' 
            try:   
                li['Technology']=item['technology'].strip()
            except:
                li['Technology']=''  
            try:  
                ts=int(str(item['creationDate'])[:-3])
                createdOn=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                li['Created On']=createdOn
            except:
                li['Created On']=''
            try:    
                li['Supported Nomenclatures']=','.join(item['supportedNomenclatures'])
            except:
                li['Supported Nomenclatures']=''
            try:    
                li['LCIA Methods Used']=','.join(item['lciaMethods'])
            except:
                li['LCIA Methods Used']=''    
            try:
                li['Reviewers']=','.join(item['reviewers'])
            except:
                li['Reviewers']=''   
            try: 
                li['Documentor']=item['documentor']
            except:
                li['Documentor']=''  
            try: 
                li['Generator']=item['generator']
            except:
                li['Generator']=''       
            try:
                li['Inventory Modeling Type']=','.join(item['modelingType']).replace('_',' ')
            except:
                li['Inventory Modeling Type']=''       
            try:
                li['Multifunctional Modeling']=','.join(item['multifunctionalModeling']).replace('_',' ')
            except:
                li['Multifunctional Modeling']=''   
            try:
                li['Biogenic Carbon Modeling']=','.join(item['biogenicCarbonModeling']).replace('_',' ')
            except:
                li['Biogenic Carbon Modeling']=''   
            try:
                li['End of Life Modeling']=','.join(item['endOfLifeModeling']).replace('_',' ')
            except:
                li['End of Life Modeling']=''   
            try:
                li['Water Modeling']=','.join(item['waterModeling']).replace('_',' ')
            except:
                li['Water Modeling']=''   
            try:
                li['Infrastructure Modeling']=','.join(item['infrastructureModeling']).replace('_',' ')
            except:
                li['Infrastructure Modeling']=''   
            try:
                li['Emission Modeling']=','.join(item['emissionModeling']).replace('_',' ')
            except:
                li['Emission Modeling']=''   
            try:
                li['Carbon Storage Modeling']=','.join(item['carbonStorageModeling']).replace('_',' ')
            except:
                li['Carbon Storage Modeling']=''   
            try:
                li['Review Type']=','.join(item['reviewType']).replace('_',' ')
            except:
                li['Review Type']=''   
            try:
                li['Review System']=','.join(item['reviewSystem']).replace('_',' ')
            except:
                li['Review System']=''   
            try:
                li['Process Type']=','.join(item['processType']).replace('_',' ')
            except:
                li['Process Type']=''   
            try:
                li['Representativeness Type']=','.join(item['representativenessType']).replace('_',' ')
            except:
                li['Representativeness Type']=''   
            try:
                li['Source Reliability']=','.join(item['sourceReliability']).replace('_',' ')
            except:
                li['Source Reliability']=''   
            try:
                li['Aggregation Type']=','.join(item['aggregationType']).replace('_',' ')
            except:
                li['Aggregation Type']=''       
            
          


            #self.datasets.append(li)
            yield li


        #navigate to next page
        headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.9'
                  } 
        totalPages=json_data['resultInfo']['pageCount']
        currentPage=json_data['resultInfo']['currentPage']        
        if(currentPage<totalPages):      
            #print("Next Page-----------")
            currentPage+=1
            #print('URL ------------------------------->',response.request.url)
            url=response.request.url.split('&')[0]+'&page='+str(currentPage)
            yield scrapy.Request(url,method='GET', callback=self.parseItem,headers=headers) 


    # def closed(self, reason):
    #         # will be called when the crawler process ends
    #         # any code 
    #         # do something with collected data 
    #     df = pd.DataFrame(self.datasets)
    #     print(df)
    #     df.to_csv(self.name+'.csv',index=False)         