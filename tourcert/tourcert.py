import re
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import scrapy
import pandas as pd
import xmltodict
import json
import datetime

class tourcertSpider(scrapy.Spider):
    name='tourcert'
    allowed_domains = ['tourcert.org']
    start_urls=['https://tourcert.org/wp-content/themes/tc_theme/search-ajax-test.php?page=1&vis=0&typ=undefined&s=&cat=&cert=&lang=en']
    start=0
    total=32
 

    def parse(self, response):   
        for item in response.xpath('//div[@class="community-card cb-shadow"]'):
            url='https://tourcert.org/en/community/'+item.xpath('./a/@href').get().strip()+'/'
            #print('url-----',url)
            yield scrapy.Request(url, callback=self.parseItem)

        #next page
        self.start+=1
        if(self.start<=self.total):
            url=re.sub(r'page=[\d]+','page='+str(self.start),self.start_urls[0])
            print('next url-----',url)
            yield scrapy.Request(url,method='GET', callback=self.parse)      

        

    def parseItem(self,response):
        li={}
        li['URL']=response.request.url
        
        
        li['Community Name']=response.xpath('//p[@class="community-name"]/text()').get().strip()
        
        try:
            li['Community Type']=response.xpath('//span[@class="community-type"]/text()').get().strip()
        except:
            li['Community Type']=''    

        li['About']=''.join([replace_escape_chars(para) for para in response.xpath('//div[@class="community-content"]/p//text() | //div[@class="community-content"]/div[@class="ewa-rteLine"]//text()').extract()])
        
        for item in response.xpath('//div[@class="col-lg-2 offset-lg-2 member-description"]/p[@class="community-left-h"]'):
            key=item.xpath('./text()').get()
            #print('key----------------',key)
            if(key=='Share'):
                value=','.join(val.strip() for val in item.xpath('following-sibling::p[@class="community-left-p"][1]/a/@href').extract() if  val.strip()!='')
            else:
                value=','.join(val.strip() for val in item.xpath('following-sibling::p[@class="community-left-p"][1]//text()').extract() if  val.strip()!='')
                value=value.replace(',@,','@')

            if(key and value and key!="" and value!=""):
                li[key.strip()]=value.strip()



        for item in response.xpath('//div[@class="community-tax"]'):
            key=item.xpath('./p[@class="community-tax-h text-center"]/text()').get()
            #print('key----------------',key)
            value=','.join(val.strip() for val in item.xpath('./p[@class="community-tax-p text-center"]//text()').extract() if  val.strip()!='')
            if(key and value and key!="" and value!=""):
                li[key.strip()]=value.strip()
         


        yield li      

        
           