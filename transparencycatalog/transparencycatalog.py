from logging import exception
import scrapy
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import re

class TransparencycatalogSpider(scrapy.Spider):
    name = 'transparencycatalog'
    allowed_domains = ['transparencycatalog.com']
    start_urls = ['https://www.transparencycatalog.com/']
# https://www.transparencycatalog.com/products/ise-logik-industries
    def parse(self, response):
        urls=response.xpath('//div[@class="column-brands"]/p/a/@href').extract()
        for url in urls:
            url='https://www.transparencycatalog.com/products/'+url.split('/')[-1]
            yield scrapy.Request(url, callback=self.parseItem)


    def parseItem(self, response):
        if response.xpath('//table[contains(@class,"tabs-table tabs-body-table table-shadow")]/tbody'):
            for body in response.xpath('//table[contains(@class,"tabs-table tabs-body-table table-shadow")]/tbody'):
                for row in body.xpath('tr[contains(@class,"levels_row ")]'):
                    li={}
                    li['URL']=re.sub('products','company',response.url)
                    try:
                        li['Product']=replace_escape_chars(row.xpath('./th/div/span/a/text()').get())
                    except:
                        li['Product']=''
                    if li['Product']=='':
                        li['Product']=replace_escape_chars(row.xpath('./th/div/span//text()').get())
                    for i in range(1,4):
                        li['EP-PROGRAM']=''
                        li['EP-SCOPE']=''
                        li['EP-EXPIRES']=''
                        li['MI-PROGRAM']=''
                        li['MI-SCOPE']=''
                        li['MI-EXPIRES']=''
                        try:
                            li['EP-PROGRAM']=replace_escape_chars(''.join([item.strip() for item in row.xpath('./td[contains(@class,"bck_material")]/div['+str(i)+']/div[1]/div//text()').extract()]))
                            li['EP-PROGRAM URL']=row.xpath('./td[contains(@class,"bck_material")]/div['+str(i)+']/div[1]/div/a/@href').get()
                            li['EP-SCOPE']=replace_escape_chars(''.join([item.strip() for item in row.xpath('./td[contains(@class,"bck_material")]/div['+str(i)+']/div[2]/div/text()').extract()]))
                            li['EP-EXPIRES']=replace_escape_chars(row.xpath('./td[contains(@class,"bck_material")]/div['+str(i)+']/div[3]/div/text()').get())
                        except:
                            print('ignore')
                            

                        try:
                            li['MI-PROGRAM']=replace_escape_chars(''.join([item.strip() for item in row.xpath('./td[contains(@class,"material_ingredients")]/div['+str(i)+']/div[1]//text()').extract()]))
                            li['MI-PROGRAM URL']=row.xpath('./td[contains(@class,"material_ingredients")]/div['+str(i)+']/div[1]/a/@href').get()
                            li['MI-SCOPE']=replace_escape_chars(''.join([item.strip() for item in row.xpath('./td[contains(@class,"material_ingredients")]/div['+str(i)+']/div[2]/text()').extract()]))
                            li['MI-EXPIRES']=replace_escape_chars(row.xpath('./td[contains(@class,"material_ingredients")]/div['+str(i)+']/div[3]/div/text()').get())
                        except:
                            print('ignore')

                        if li['EP-PROGRAM']=='' and li['EP-SCOPE']=='':
                            li['EP-EXPIRES']=''

                        if all(li[k]=='' or li[k]==None for k in list(li.keys())[2:]):
                            continue
                        else:
                            yield li

        else:
            for row in response.xpath('//table[contains(@class,"tabs-table tabs-body-table table-shadow")]//tr[contains(@class,"levels_row ")]'):
                    li={}
                    li['URL']=re.sub('products','company',response.url)
                    try:
                        li['Product']=replace_escape_chars(row.xpath('./th/div/span/a/text()').get())
                    except:
                        li['Product']=''

                    if li['Product']=='':
                        li['Product']=replace_escape_chars(row.xpath('./th/div/span//text()').get())
                    for i in range(1,4):
                        li['EP-PROGRAM']=''
                        li['EP-SCOPE']=''
                        li['EP-EXPIRES']=''
                        li['MI-PROGRAM']=''
                        li['MI-SCOPE']=''
                        li['MI-EXPIRES']=''
                        try:
                            li['EP-PROGRAM']=replace_escape_chars(''.join([item.strip() for item in row.xpath('./td[contains(@class,"bck_material")]/div['+str(i)+']/div[1]/div//text()').extract()]))
                            li['EP-PROGRAM URL']=row.xpath('./td[contains(@class,"bck_material")]/div['+str(i)+']/div[1]/div/a/@href').get()
                            li['EP-SCOPE']=replace_escape_chars(''.join([item.strip() for item in row.xpath('./td[contains(@class,"bck_material")]/div['+str(i)+']/div[2]/div/text()').extract()]))
                            li['EP-EXPIRES']=replace_escape_chars(row.xpath('./td[contains(@class,"bck_material")]/div['+str(i)+']/div[3]/div/text()').get())
                        except:
                            print('ignore')
                            

                        try:
                            li['MI-PROGRAM']=replace_escape_chars(''.join([item.strip() for item in row.xpath('./td[contains(@class,"material_ingredients")]/div['+str(i)+']/div[1]//text()').extract()]))
                            li['MI-PROGRAM URL']=row.xpath('./td[contains(@class,"material_ingredients")]/div['+str(i)+']/div[1]/a/@href').get()
                            li['MI-SCOPE']=replace_escape_chars(''.join([item.strip() for item in row.xpath('./td[contains(@class,"material_ingredients")]/div['+str(i)+']/div[2]/text()').extract()]))
                            li['MI-EXPIRES']=replace_escape_chars(row.xpath('./td[contains(@class,"material_ingredients")]/div['+str(i)+']/div[3]/div/text()').get())
                        except:
                            print('ignore')

                        if li['EP-PROGRAM']=='' and li['EP-SCOPE']=='':
                            li['EP-EXPIRES']=''

                        if all(li[k]=='' or li[k]==None for k in list(li.keys())[2:]):
                            continue
                        else:
                            yield li