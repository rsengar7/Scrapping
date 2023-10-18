# -*- coding: utf-8 -*-
import json
import re
from typing import ItemsView
import scrapy
from csv import DictWriter
import os
from ast import literal_eval
from ASI.items import ProductLoader
from ASI.format import formatter
import pandas as pd
import xmltodict
from extruct import JsonLdExtractor
from itemloaders.processors import SelectJmes as pick

class ConceptsurfacesSpider(scrapy.Spider):
    name = 'conceptsurfaces'
    allowed_domains = ['conceptsurfaces.com']
    start_urls = ['https://conceptsurfaces.com/products/porcelain-tile/floor/','https://conceptsurfaces.com/products/porcelain-tile/wall/','https://conceptsurfaces.com/products/porcelain-tile/gauge-tile-panels/','https://conceptsurfaces.com/products/mosaics/glass/','https://conceptsurfaces.com/products/mosaics/metallic/','https://conceptsurfaces.com/products/mosaics/floor/','https://conceptsurfaces.com/products/mosaics/wall/']

    def parse(self, response):
        for url in response.xpath('//div[@id="tile-wrapper"]/div/div/div/@data-series-link').extract():
            # url=item.xpath('./@href').get()
            url='https://conceptsurfaces.com'+url
            yield scrapy.Request(url, callback=self.parseItem)

    def parseItem(self,response):
            variants = self.parse_variants(response)
            for variant in variants:
                specifications=self.Specificationsalt(response) 
                # print(specifications)
                for key in specifications.keys():
                    # print(key)
                    li = ProductLoader(response=response)
                    li.add_xpath('name','//div[@class="large-12 medium-12 small-12 text-center columns inner"]/h1/text()')
                    li.add_value('sku',li.get_collected_values('name')[0]+'-'+variant['sku']+'-'+key) 
                    li.add_value("main_image", variant['main_image'])
            
                    li.add_value('url',response.request.url)

                    li.add_value('brand', 'Concept Surfaces')
                    li.add_value('breadcrumbs',response.request.url.title().split('/')[4:-1])
                    li.add_xpath("image_urls",'//div[@class="large-4 medium-4 small-12 columns inspiration-item"]/@data-url' )
                    if(li.get_collected_values("image_urls")==[]):
                        li.add_xpath("image_urls",'//div[@class="large-4 medium-4 small-12 columns inspiration-item end"]/@data-url' )
                    print(li.get_collected_values('image_urls'))
                    
                    li.add_xpath("file_urls",'//div[@id="sidebar-img"]/div/a/@href' )
                    spec=self.Specifications(specifications[key],variant)
                    li.add_value('specifications',spec)
                    
                    yield li.load_item()
            
    def parse_files(self,response):
        files=response.xpath('//div[@id=""sidebar-img""]/div/a/@href').extract()  
        return files
    
    def parse_variants(self, response):
        variants = []

        for item in response.xpath('//div[@class="series large-4 medium-4 small-12 columns end "]/div/div/div/ul'):
            variant = {}
            variant["sku"] = item.xpath('./li[2]/@data-title').get().strip()
            variant["main_image"] = item.xpath('./li[2]/@data-image').get()
            variant["finish"]=item.xpath('./li[1]/a/@data-finish').get().strip()
            variant["size"]=item.xpath('./li[1]/a/@data-sizes').get().strip()
            variants.append(variant)
        if(variants==[]):
            for item in response.xpath('//div[@class="series large-4 medium-4 columns end"]/div/div/div/ul'):
                variant = {}
                variant["sku"] = item.xpath('./li[2]/@data-title').get().strip()
                variant["main_image"] = item.xpath('./li[2]/@data-image').get()
                variant["finish"]=item.xpath('./li[1]/a/@data-finish').get().strip()
                variant["size"]=item.xpath('./li[1]/a/@data-sizes').get().strip()
                variants.append(variant)
        return variants   

    def Specificationsalt(self,response):
        specifications={}
        for item in response.xpath('//ul[@class="accordion"]/li'):
            mainKey=item.xpath('./a/text()').get()
            fields=item.xpath('./div/div/ul/li/text()').extract()
            specs={}
            for i in range(0,len(fields),2):
                specs[fields[i]]=fields[i+1]
            specifications[mainKey]=specs
        return specifications
    
    @formatter
    def Specifications(self,specifications,variant):
        
        specifications['Finish']=variant['finish']
        specifications['Size']=variant['size']
        return specifications