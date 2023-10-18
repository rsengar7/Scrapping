# -*- coding: utf-8 -*-
import json
import re
import scrapy
from csv import DictWriter
import os
from ast import literal_eval

from scrapy.http import request
from ASI.items import ProductLoader
from itemloaders.processors import Compose, Join
from w3lib.html import remove_tags, replace_entities, replace_escape_chars


from ASI.format import formatter
import pandas as pd
import xmltodict
from extruct import JsonLdExtractor
from itemloaders.processors import SelectJmes as pick
import html

class ArchitessaSpider(scrapy.Spider):
    name = 'architessa'
    allowed_domains = ['architessa.com']
    start_urls = ['https://architessa.com/sitemap_products_1.xml?from=5487771779233&to=7077139054753']
    def parse(self, response):
        # count=1
        raw = xmltodict.parse(response.text)
        data = [r["loc"] for r in raw["urlset"]["url"]]
        for url in data:
            if 'products/' in url:
                # count=count+1
                # if count<5:
                    yield scrapy.Request(url, callback=self.parseItem)
        # yield scrapy.Request('https://architessa.com/products/astoria?variant=41040398221473', callback=self.parseItem)
        
    def parseItem(self,response):
        jsonStr=json.loads(re.findall(r'window.SwymProductInfo.product = ({.*});',response.text)[0])
        variantJSON=jsonStr['variants']
            
        for variant in variantJSON: 
            # print(variant)
                li = ProductLoader(response=response)
                if variant['sku']=='':
                    li.add_value('sku',jsonStr['title'])
                    li.add_value("main_image", jsonStr['featured_image'])

                else:    
                    li.add_value('sku',variant['sku'])
                    try:
                        li.add_value("main_image", variant['featured_image']['src'])
                    except:
                        li.add_value("main_image", jsonStr['featured_image'])

                li.add_value("name",variant['name'].strip())
                li.add_value('url',response.request.url+'?variant='+str(variant['id']))
                # description=replace_escape_chars(' '.join(response.xpath('//div[@class="summary__short"]/p//text()').extract()))
                # description=replace_entities(remove_tags(jsonStr['description'])).replace(r'\\u003cp\\u003e','').replace('<p>','')
                try:
                    description=replace_escape_chars(remove_tags(jsonStr['description']))
                except:
                    description=''
                li.add_value("description",description)
                li.add_value('brand', 'Architessa') 
                li.add_value('breadcrumbs',[jsonStr['type'],jsonStr['title']])
                li.add_value("colour",variant['option1'])

                li.add_value("image_urls",['https:'+image for image in jsonStr['images']])
                resources=[link for link in response.xpath('//div[@class="custom-accordion-column"]/a/@href').extract() if '.pdf' in link]
                li.add_value("file_urls",resources )
                specifications=self.Specifications(response)
                li.add_value('specifications',specifications)
                yield li.load_item()
       
      
      
    @formatter
    def Specifications(self,response):
        specifications={}
        text = [
            ' '.join(
                line.strip() 
                for line in p.xpath('.//text()').extract() 
                if line.strip()
            ) 
            for p in response.xpath('//div[@data-toggle="specifications"]/div/p')
        ]
        # print(text)
        for item in text:
            if ':' in item:
                keyValue=item.split(':')
                key=keyValue[0].strip()
                value=keyValue[1].strip()
                if(key!='' and value!=''):
                    specifications[key]=value
        return specifications

