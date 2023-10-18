import scrapy
import json
import re
from w3lib.html import remove_tags, replace_entities, replace_escape_chars

class IbuEpdSpider(scrapy.Spider):
    name = 'ibu-epd'
    allowed_domains = ['ibu-epd.com','ibudata.lca-data.com']
    start_urls = ['https://ibudata.lca-data.com/resource/datastocks/7f92c48a-07c6-4a0c-91fd-4166e6138402/processes?format=json&search=true&startIndex=0&pageSize=50&sortOrder=true&sortBy=name&validUntil=2022']
    currentIndex=0
    
    def parse(self, response):
        response_json=json.loads(response.text)
        for product in response_json['data']:
            url='https://ibudata.lca-data.com/datasetdetail/process.xhtml?uuid='+product['uuid']+'&version='+product['version']+'&stock=PUBLIC&lang=de'
            # yield {'url':url}
            yield scrapy.Request(url, callback=self.parseItem)

        if self.currentIndex<response_json['totalCount']:
            currentIndexLink='startIndex='+str(self.currentIndex)

            nextIndex=self.currentIndex+50
            nextIndexLink='startIndex='+str(nextIndex)
            url=response.request.url.replace(currentIndexLink,nextIndexLink)
            self.currentIndex=nextIndex
            # print('xxxxxxxxxxxxxx',payload)
            yield scrapy.Request(url=url,callback=self.parse)


    def parseItem(self,response):
        li={}
        li['URL']=response.request.url
        specifications={}
        for item in response.xpath('//table[@id="j_idt62:accPanel:j_idt105"]//tr'):
            key=item.xpath('./td[1]/span/span/text()').get()
            # value=re.sub(r'\$\(function\(\).*?;','',''.join(item.strip() for item in item.xpath('./td[2]//text()').extract())).replace('});',' ')
            value=re.sub(r'\$\(function\(\).*?;','',''.join(' '.join(item.split()).strip() for item in item.xpath('./td[2]//text()').extract())).replace('});',' ')
            if(key!=None and value !=None and len(key)>0 and len(value.strip())>0):
                    specifications[key.strip()]=value.strip()

        # for item in response.xpath('//div[@class="product-dimensions"]/ul/li'):
        #     key=item.xpath('./b/text()').get()
        #     value=item.xpath('./text()').get()
        #     if(key!=None and value !=None):
        #             specifications[key.strip()]=value.strip()

        li.update(specifications)
        
        yield li
