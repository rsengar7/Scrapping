import re
import scrapy
import re
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import json

class CasafinagiftsSpider(scrapy.Spider):
    name = 'casafinagifts'
    allowed_domains = ['casafinagifts.com']
    start_urls = ['https://www.casafinagifts.com/api/api.php/getProducts/442/414/0']

    def parse(self, response):
        json_data=json.loads(response.text)
        for product in json_data['response']['products']:
            li={}
            li['URL']=product['url']
            li['Name']=product['title']
            li['SKU']=product['sku']
            li['Description']=product['content'].replace('<br>',' | ')
            li['Price']=product['price']['value']
            li['Brand']= 'Casafina Gifts'
            li['Breadcrumbs']=['PRODUCTS',li['Name']]
            li['Use']=product['composition']['CARE'][0]['feature']
            
            li["Image URLs"]=[]
            try:
                for image in product['images']:
                    temp={}
                    temp['Item_Image']='https://www.casafinagifts.com/'+image['resource_url']['thumb']
                    temp['Detailed_Image']='https://www.casafinagifts.com/'+image['resource_url']['small']
                    temp['Zoom_Image']='https://www.casafinagifts.com/'+image['resource_url']['regular']
                    li["Image URLs"].append(temp)
            except:
                li["Image URLs"]=[]
            for key,variant in product['available_colors'].items():
                print(variant,key)
                li['URL']=variant['url']
                li['SKU']=variant['sku']
                li['Color']=variant['short_name']
                try:
                    temp={}
                    temp['Item_Image']='https://www.casafinagifts.com/'+variant['image']['resource_url']['thumb']
                    temp['Detailed_Image']='https://www.casafinagifts.com/'+variant['image']['resource_url']['small']
                    temp['Zoom_Image']='https://www.casafinagifts.com/'+variant['image']['resource_url']['regular']
                    li["Image URLs"].append(temp)
                except:
                    pass
                yield li

            split_url=response.request.url.split('/')
            next_page=int(split_url[-1])+12

            if(next_page<int(json_data['response']['products_count'])):
                split_url[-1]=str(next_page)
                url='/'.join(split_url)
                yield scrapy.Request(url, callback=self.parse)

            