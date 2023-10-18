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


class MasterSpider(scrapy.Spider):
    name = 'master'
    allowed_domains = ['master.ca']
    start_urls = ['https://www.master.ca/professional/residential?p=1','https://www.master.ca/professional/commercial-industrial?p=1','https://www.master.ca/professional/motors-and-fans?p=1','https://www.master.ca/professional/tools-and-maintenance?p=1',]
    completeProducts=[]

    def parse(self, response):
        links=response.xpath('//a[@class="product photo product-item-photo"]/@href').extract()
        for link in links:
            yield scrapy.Request(link,callback=self.parseItem)
        print(links,len(links))
        nextPage=response.xpath('//a[@class="action  next"]/@href').get()
        if nextPage:
            yield scrapy.Request(nextPage)

    def parseItem(self,response):
        # print(response.text)
        li={}
        li['Description']=replace_escape_chars(' '.join(response.xpath('//div[@class="product attribute description"]/div[1]/text()').extract())).strip()
        li['SKU']=response.xpath('//div[@class="product attribute sku"]/div/text()').get()
        li['URL']=response.request.url
        li['Title']=response.xpath('//h1[@class="page-title"]/span/text()').get().strip()
        li['Sub Title']=response.xpath('//div[@class="product attribute overview content"]/div/text()').get().strip()
        li['breadcrumbs']=['Home',li['Title']]
        li['Brand']= 'Master'
        li['Specification']=self.Specifications(response)
        li['Brand']=li['Specification'].get('Brand')
        li['Images']=', '.join([image for image in response.xpath('//meta[@property="og:image"]/@content').extract()])

        self.completeProducts.append(li)


    def Specifications(self,response):
        specifications={}
        for spec in response.xpath('//div[@class="additional-attributes-wrapper table-wrapper"]/table//tr'):
            key=unicodedata.normalize("NFKD", spec.xpath('./th/text()').get())
            value=spec.xpath('./td/text()').get()
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