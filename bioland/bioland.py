import re
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import scrapy
import pandas as pd
import xmltodict
import json
import datetime

class biolandSpider(scrapy.Spider):
    name='bioland'
    allowed_domains = ['https://www.bioland.de/']
    start_urls = ['https://www.bioland.de/index.php?eID=conlabz_bioland_data/biolandmaps/Maps/search']
    companies=[]
    
    def start_requests(self):
        headers = {
                    'accept': '*/*',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
                   }


        payload = "freetext=&tx_conlabzbiolanddata_biolandmaps%5B__referrer%5D%5B%40extension%5D=ConlabzBiolandData&tx_conlabzbiolanddata_biolandmaps%5B__referrer%5D%5B%40controller%5D=Maps&tx_conlabzbiolanddata_biolandmaps%5B__referrer%5D%5B%40action%5D=index&tx_conlabzbiolanddata_biolandmaps%5B__referrer%5D%5Barguments%5D=YTowOnt9cadd4668ac7edb48e02325bb303f76b6d7db7b2c&tx_conlabzbiolanddata_biolandmaps%5B__referrer%5D%5B%40request%5D=%7B%22%40extension%22%3A%22ConlabzBiolandData%22%2C%22%40controller%22%3A%22Maps%22%2C%22%40action%22%3A%22index%22%7Db047eb2a8e756922677049497bd5dd5dbf028c66&tx_conlabzbiolanddata_biolandmaps%5B__trustedProperties%5D=%7B%22location%22%3A1%7Da42cf01622e6cad210549ee96d8b344fcb889989&tx_conlabzbiolanddata_biolandmaps%5Blocation%5D=&tx_conlabzbiolanddata_biolandmaps%5Blongitude%5D=1.951110839843752&tx_conlabzbiolanddata_biolandmaps%5Blatitude%5D=49.230153752280884&tx_conlabzbiolanddata_biolandmaps%5Bcorner1long%5D=-3.632751464843751&tx_conlabzbiolanddata_biolandmaps%5Bcorner1lat%5D=289.834439500479235&tx_conlabzbiolanddata_biolandmaps%5Bcorner2long%5D=50.26947021484375&tx_conlabzbiolanddata_biolandmaps%5Bcorner2lat%5D=1.61838518688487"            
      
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for url in self.start_urls:
            # Uses the Scraper API service to get the source data. Scraper API is a service which uses proxy to bypass bot detection. 
            yield scrapy.Request(url,method='POST', callback=self.parseItem,headers=headers,body=payload)


    def parseItem(self, response):
        json_data=json.loads(response.text)
        #print(json_data)

        for item in json_data['results']:
            li={}
            li['uid']=item['uid']
            li['pid']=item['pid']
            li['Status']=item['status']
            li['Created']=item['created']
            li['Updated']=item['updated']
            li['Category']=item['category']
            li['Country']=item['country']
            li['State']=item['state']
            li['Company Name 1']=item['company_name1']
            li['Company Name 2']=item['company_name2']
            li['FAX Headoffice']=item['fax_headoffice']
            li['Email']=item['email_headoffice']
            li['Address Type']=item['address_type']
            li['Delivery Radius']=item['deliveryradius']
            li['Facebook']=item['facebook']
            li['Instagram']=item['instagramm']
            li['Twitter']=item['twitter']
            li['Phone_central']=item['phone_central']
            li['Phone_mobil']=item['phone_mobil']
            li['Phone_business']=item['phone_business']
            li['Street']=item['street']
            li['City Part']=item['city_part']
            li['City']=item['city']
            li['Homepage']=item['homepage']
            li['Zip']=item['zip']
            li['Features']=item['features']
            li['Table Names']=item['tablenames']
            li['Offer']=item['offer']
            li['Products']=item['products']
            li['Distance']=item['distance']



            self.companies.append(li)


    def closed(self, reason):
            # will be called when the crawler process ends
            # any code 
            # do something with collected data 
        df = pd.DataFrame(self.companies)
        print(df)
        df.to_csv(self.name+'.csv',index=False)         








            





            





        