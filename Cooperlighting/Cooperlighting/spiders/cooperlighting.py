# -*- coding: utf-8 -*-
from typing import ItemsView
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup, element
import re
import httplib2
from itertools import product
from requests.models import codes
import scrapy
from csv import DictWriter
import os
import time

from scrapy.http import headers
from scrapy.utils.trackref import NoneType

class CooperlightingSpider(scrapy.Spider):
    name = 'cooperlighting'
    allowed_domains = ['cooperlighting.com']
    start_urls = ['https://www.cooperlighting.com/global.product-sitemap.xml']

    def parse(self, response):
        totalLinks=re.findall(r'(https?://\S+?)<', str(response.body))
        for i in range(len(totalLinks)):
            yield scrapy.Request(totalLinks[i],callback=self.parseProduct)

    def Specification(self, response):
        totalJSON = '{'
        seperatedJSON = ''
        res=response.xpath('//tr[@class="product-specifications__row"]/td/span/text()').extract()
        for i in range(0,len(res),2):
            key = res[i]
            value = res[i+1]
            seperatedJSON = seperatedJSON+'"'+key+'":"'+value+'",'

        totalJSON = totalJSON+seperatedJSON[:-1]+'}'

        if totalJSON == '{}':
            totalJSON='Not Available'
        self.itemToReturn = totalJSON
        return self.itemToReturn
    
    def Resources(self, response):
        totalJSON = '{'
        seperatedJSON = ''
        links=re.findall(r',title:(.*?),.*?downloadUrl:(.*?)}',response.text.replace('&#34;',''))
        # titles=re.findall(r',title:(.*?),',response.text.replace('&#34;',''))
        
        for i in range(len(links)):
            if links[i][0]:
                if 'https' in links[i][1]:
                    value=links[i][1]
                    key=links[i][0]
                    seperatedJSON = seperatedJSON+'"'+key+'":"'+value+'",'
                else:
                    value='https://www.cooperlighting.com'+links[i][1]
                    key=links[i][0]        
                    seperatedJSON = seperatedJSON+'"'+key+'":"'+value+'",'                       

        totalJSON = totalJSON+seperatedJSON[:-1]+'}'
        # print(totalLinks,len(totalLinks))
        # print(titles,len(titles))
        if totalJSON == '{}':
            totalJSON='Not Available'
        
        self.itemToReturn = totalJSON
        
        return self.itemToReturn

    def Videos(self, response):
        totalJSON = '['
        seperatedJSON = ''
        links=re.findall(r'videoUrl:(.*?),',response.text.replace('&#34;',''))
        for link in links:
            value = link.replace("'",'')
            seperatedJSON = seperatedJSON+'"'+value+'",'
        totalJSON = totalJSON+seperatedJSON[:-1]+']'

        self.itemToReturn = totalJSON if totalJSON != '[]' else 'Not Available'
        return self.itemToReturn
    
    def Images(self, response):
        seperatedJSON = ''
        res=response.xpath('//div[@class="swiper-slide-image"]/@style').extract()
        for link in res:
            largeImage=re.findall(r'background-image:url\((.*?)\?',link.replace('\\2f','/'))[0].replace(' ','')
            seperatedJSON = seperatedJSON + ' {"Item_Image":"'+largeImage+'","Detailed_Image":"' + largeImage+'","Zoom_Image":"'+largeImage+'"},'
        self.itemToReturn = '['+seperatedJSON[:-1]+']'
        if(self.itemToReturn == '[]'):
            self.itemToReturn = 'Not Available'
        return self.itemToReturn
    
    def writeToFile(self, item):
        field_names = ['Product URL', 'SKU', 'Title','Brand', 'Breadcrumb', 'Features','Overview','Specification','Resources','Images','Videos','Other Informations','Compatible Products']
        filename = 'CooperlightingProducts.csv'
        for key,val in item.items():
            if val==None or val=='':
                item[key]='Not Available'

        if os.path.isfile(filename):
            with open(filename, 'a', encoding='utf-8', newline='') as f_object:
                dictwriter_object = DictWriter(
                    f_object, fieldnames=field_names)
                dictwriter_object.writerow(item)
                f_object.close()
        else:
            with open(filename, 'a', encoding='utf-8', newline='') as f_object:
                dictwriter_object = DictWriter(
                    f_object, fieldnames=field_names)
                dictwriter_object.writeheader()
                dictwriter_object.writerow(item)
                f_object.close()

    def parseProduct(self, response):
        item = {}
        item['Product URL']= response.request.url      
        item['Title'] = response.xpath('//h1[@class="product-detail__title heading-3"]/text()').get()
        item['SKU'] = re.findall(r'\/brands\/.*?\/(.*?)\/',response.request.url)[0] 
        if(item['SKU']):
            item['SKU']='["'+item['SKU']+'"]'
        item['Brand'] = response.xpath('//h2[@class="product-detail__brand body-copy-1--bold"]/a/text()').get()
        item['Breadcrumb'] = '/'.join(list(dict.fromkeys(response.xpath('//li[@class="product-breadcrumbs-component__item"]/a/text()').extract())))
        item['Features']='|'.join([re.sub(r'\s\s+|\n|\xa0', ' ',item) for item in response.xpath('//div[@class="rich-text-content"]/ul/li/text()').extract()]).strip()
        item['Overview']=response.xpath('//p[@class="product-detail__description product-detail__description-text "]/text()').get()
        item['Specification']=self.Specification(response)
        item['Resources'] = self.Resources(response)
        item['Videos']=self.Videos(response)
        item['Images']=self.Images(response)
        item['Other Informations']='\n'.join([re.sub(r'\s\s+|\n|\xa0', ' ',item) for item in response.xpath('//p[@class="rich-text-content"]/text()').extract()]).strip()
        item['Compatible Products']='","'.join([re.sub(r'\s\s+|\n|\xa0', ' ',item) for item in response.xpath('//div[@class="product-card__title heading-6"]/text()').extract()]).strip()
        if(item['Compatible Products']):
            item['Compatible Products']='["'+item['Compatible Products']+'"]'
            
        self.writeToFile(item)
        
        # except TypeError as e:
            # print('-------NOT PRODUCT LINK', e)
