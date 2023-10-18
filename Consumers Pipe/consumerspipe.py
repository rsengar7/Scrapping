# -*- coding: utf-8 -*-
import json
from posixpath import join
import re
import scrapy
from csv import DictWriter
import os
from ast import literal_eval
import pandas as pd
import xmltodict
from extruct import JsonLdExtractor
from itemloaders.processors import Compose, SelectJmes as pick
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import collections
import os
from csv import DictWriter
import unicodedata


class ConsumerspipeSpider(scrapy.Spider):
    name = 'consumerspipe'
    allowed_domains = ['consumerspipe.com']
    start_urls = ['https://www.consumerspipe.com/products']
    # start_urls = ['https://www.consumerspipe.com/catalog/shop/Valves/Iron/Globe-Angle-Valves/dept-5UY']
    completeProducts=[]

    def parse(self, response):
        links=response.xpath('//div[@class="image"]/a/@href').extract()
        # links=response.xpath('//div[@class="catDDHead"]/a/@href').extract()
        for link in links:
            link='https://www.consumerspipe.com/'+link
            if 'a=1' in link:
                link=link+'&itemsperpage=100&pagenum=1'
                yield scrapy.Request(link, callback=self.products)
            elif 'buy/' in link:
                print('hereee')
                yield scrapy.Request(link, callback=self.parseItem)
            else:
                yield scrapy.Request(link, callback=self.parse)

    def products(self,response):
        links=response.xpath('//div[@class="image"]/a/@href').extract()
        if links !=[]:
            for link in links:
                link='https://www.consumerspipe.com/'+link
                yield scrapy.Request(link, callback=self.parseItem)

            currentPage=int(response.request.url[-1])
            nextPage=response.request.url[:-1]+str(currentPage+1)
            yield scrapy.Request(nextPage, callback=self.products)

    def parseItem(self,response):
        li={}
        li.update(self.otherSpecifications(response))
        li['Description']=replace_escape_chars(' '.join(response.xpath('//div[@class="description"]//text()').extract())).strip()
        if 'Description:' in li['Description'] :
            li['Description']=li['Description'].split('Description:')[1].strip()
        li['breadcrumbs']=[unicodedata.normalize("NFKD", replace_escape_chars(item.strip())) for item in response.xpath('//*[@class="breadcrumblink"]//text()').extract()]
        # li['SKU']=response.xpath('//h4[@class="h3"]/text()').extract()[1]
        li['URL']=response.request.url
        li['Features']=', '.join([item for item in response.xpath('//div[@id="features"]/ul/li/text()').extract()])
        li['Name']=response.xpath('//h1[@class="pageName"]/text()').get()
        li['Brand']= 'Consumers Pipe & Supply Co.'
        li['Specification']=self.Specifications(response)
        li['Package Details']=self.packageDetails(response)
        li['Resources']=self.Resources(response)
        li['Images']=', '.join([image for image in response.xpath('//div[@class="image-box"]/a/@href').extract() if '.gif' not in image])

        self.completeProducts.append(li)
    
    def otherSpecifications(self,response):
        specifications={}
        print('----------------------')
        text = [
            ' '.join(
                line.strip() 
                for line in p.xpath('.//text()').extract() 
                if line.strip()
            ) 
            for p in response.xpath('//div[@class="description-box"]/p')
        ]
        for item in text:
            if ':' in item:
                keyValue=item.split(':')
                key=keyValue[0].strip()
                value=keyValue[1].strip()
                if(key!='' and value!=''):
                    specifications[key]=value
        return specifications

    def Specifications(self,response):
        specifications={}
        for spec in response.xpath('//div[@id="spectable"]/table//tr'):
            key=unicodedata.normalize("NFKD", spec.xpath('./td[1]/text()').get())
            value=spec.xpath('./td[2]/text()').get()
            if(key!=None and value !=None):
                specifications[key]=value
        return specifications

    def Resources(self,response):
        specifications={}
        for spec in response.xpath('//div[@id="resourcetable"]/table//tr'):
            key=spec.xpath('./td/a/text()').get()
            value=spec.xpath('./td/a/@href').get()
            if(key!=None and value !=None):
                specifications[key]=value
        return specifications

    def packageDetails(self,response):
        specifications={}
        for spec in response.xpath('//div[@id="packagetable"]/table//tr'):
            key=unicodedata.normalize("NFKD", spec.xpath('./td[1]/text()').get())
            value=spec.xpath('./td[2]/text()').get()
            if(key!=None and value !=None):
                specifications[key]=value
        return specifications

    def closed(self, reason):
        # will be called when the crawler process ends
        # any code 
        # do something with collected data 
        df = pd.DataFrame(self.completeProducts)
        print(df)
        df.to_csv(self.name+'.csv')