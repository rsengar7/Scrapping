import json
import scrapy
import re
import pandas as pd

class ElkhomeSpider(scrapy.Spider):
    name = 'elkhome'
    allowed_domains = ['elkhome.com']
    start_urls = ['https://www.elkhome.com/api/v1/categories/']
    completeProducts=[]

    def parse(self, response):
        json_response=json.loads(response.text)
        sub_cat=[sub_cat for category in json_response['categories'] for sub_cat in category['subCategories'] ]
        ids=[]
        for sub_sub_cat in sub_cat:
            if 'subCategories' in sub_sub_cat and sub_sub_cat['subCategories']:
                for item in sub_sub_cat['subCategories']:
                    ids.append(item['id'])
                    # print(item['id'])

            else:
                ids.append(sub_sub_cat['id'])
        link='https://www.elkhome.com/api/v2/products?page=1&categoryId=cdc5049a-89c2-42e4-8a91-ad2e01628fd1&expand=attributes%2Cfacets%2Cimages&includeAttributes=includeOnProduct'
        for id in ids:
            # 18,33
            replace_term='categoryId='+id
            url=re.sub('categoryId=cdc5049a-89c2-42e4-8a91-ad2e01628fd1',replace_term,link)
            yield scrapy.Request(url, callback=self.parseItem)
        # yield scrapy.Request("https://www.elkhome.com/api/v2/products?page=1&categoryId=975d137c-3bfc-4f70-87d9-ad49015f64bc&expand=attributes%2Cfacets%2Cimages&includeAttributes=includeOnProduct", callback=self.parseItem)


    def parseItem(self,response):
        jsonStr=json.loads(response.text)
        productJSON=jsonStr['products']
        if productJSON!=[]:
            for product in productJSON:  
                url='https://www.elkhome.com'+product['canonicalUrl']
                yield scrapy.Request(url, callback=self.parseItemVariants)

            currentPage=int(re.findall(r'page=(.*?)&',response.request.url)[0])
            replace_term='page='+str(currentPage+1)+'&'

            url=re.sub(r'page=.*?&',replace_term,response.request.url)
            yield scrapy.Request(url, callback=self.parseItem)
    
      
      
    def parseItemVariants(self,response):
        json_response=json.loads(re.findall(r'initialReduxState = (.*})?<\/',response.text)[0])
        for key,product in json_response['data']['products']['byId'].items():
            li = {}
            li['URL']=response.request.url
            li['sku']=product['productNumber']
            li["name"]=product['productTitle']
            li["description"]=product['content']['htmlContent']
            li['breadcrumbs']=[item['children'] for item in json_response['components']['breadcrumbs']['links']]
            
            specifications={}
            try:
                for spec in product['attributeTypes']:
                    try:
                        specifications[spec['label']]=spec['attributeValues'][0]['valueDisplay']
                    except:
                        continue
                li.update(specifications)
            except:
                pass
           
            li["image_urls"]=[]
            try:
                for image in product['images']:
                    temp={}
                    temp['Item_Image']=image['smallImagePath']
                    temp['Detailed_Image']=image['mediumImagePath']
                    temp['Zoom_Image']=image['largeImagePath']
                    li["image_urls"].append(temp)
            except:
                li["image_urls"]=[]
            
            self.completeProducts.append(li)
            # yield li



    def closed(self, reason):
        # will be called when the crawler process ends
        # any code 
        # do something with collected data 
        df = pd.DataFrame(self.completeProducts)
        print(df)
        df.to_csv(self.name+'.csv')