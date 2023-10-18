import scrapy
import json
import pandas as pd
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
class SpotUlProductdetailsSpider(scrapy.Spider):
    name = 'spot.ul-productDetails'
    allowed_domains = ['spot.ul.com']
    start_urls = ['http://spot.ul.com/']
    # completeProducts=[]
    limit=100
    try:
        with open('spot.ul-productIDs.csv') as f:
            start_urls = f.readlines()
    except:
        pass


    def start_requests(self):
        headers = {
        'aid': '5a5856538404691cc28fee28',
        'authorization': 'Basic MjIzNDU2Nzg5MDp5d2VydHl1aW9wMDk4NzY1NDMyMQ==',
        'content-type': 'application/json',
        'referer': 'https://spot.ul.com/main-app/products/detail/5d92343295c1552d2462b826?page_type=Products%20Catalog',
        'accept':'application/json'
        }

        
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for prodID in self.start_urls[75000:]:
            payload = json.dumps({
            "filters": [],
            "keywords": "",
            "productId": prodID.strip()
            })

            url="https://spot.ul.com/data/spot/api/v1/en/Products/Detail/?page_type=Products%20Catalog"


            yield scrapy.Request(url,method='POST', callback=self.parseItem,headers=headers,body=payload,dont_filter=True)


    def parseItem(self,response): 
        print(response.text)
        product=json.loads(response.text)
        li={'URL':'','Name':'','Manufacturer':'','Description':'','Website':'','Contact':'','Address':'','Product Type':'','Certification':'','SPOT Partner':'','Standard Number':'','BIM Category':'','Region Sold':'','Region Manufactured':'','Email':'','Rating Systems/Sustainable Credits':'','UniFormat':'','MasterFormat®':''}
        li['URL']='https://spot.ul.com/main-app/products/detail/'+product['product_id']+'?page_type=Products%20Catalog'
        li['Name']=product['name']
        li['Manufacturer']=product['manufacturer']['name']
        try:
            li['Description']=replace_escape_chars(product['description'] )
        except:
            li['Description']=''


        if product['manufacturer']['url']:
            li['Website']=product['manufacturer']['url']
        else:
            li['Website']='NA'

          
        if product['contact']:
            li['Email']=product['contact']['email']
            li['Contact']=product['contact']['first_name'] + ' ' + product['contact']['last_name']
        else:
            li['Email']='NA'
            li['Contact']='NA'
     


        if product['manufacturer']['address']:
            li['Address']=product['manufacturer']['address']
        else:
            li['Address']='NA'    
        

        for category in product['categories']:
            key=category['group']
            if category['group'] in li and li[key.strip()]!='':
                while category['subcategories']:
                    category=category['subcategories'][0]
                li[key.strip()]=li[key.strip()]+","+category['name'].strip()
            else:
                while category['subcategories']:
                    category=category['subcategories'][0]
                li[key.strip()]=category['name'].strip()
                
        
        yield li
        # self.completeProducts.append(li)


    # def closed(self, reason):
    #         # will be called when the crawler process ends
    #         # any code 
    #         # do something with collected data 
    #     df = pd.DataFrame(self.completeProducts)
    #     print(df)
    #     df.to_csv(self.name+'.csv',index=False)         