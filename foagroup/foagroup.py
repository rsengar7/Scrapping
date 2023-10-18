from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import scrapy

class FoagroupSpider(scrapy.Spider):
    name = 'foagroup'
    allowed_domains = ['foagroup.com']
    start_urls = ['https://www.foagroup.com/']

    def parse(self, response):
        urls=response.xpath('//a[@class="level-top"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_sub_categories)

    def parse_sub_categories(self, response):
        sub_category_urls=response.xpath('//a[@class="category-list-product-img"]/@href').extract()
        for url in sub_category_urls:
            url=url+"?p=1"
            yield scrapy.Request(url, callback=self.get_Product_urls)


        
    def get_Product_urls(self,response):
        product_urls=response.xpath('//div[@class="product-img-box"]/a/@href').extract()
        for url in product_urls:
            yield scrapy.Request(url, callback=self.parseItem)

        next_page=response.xpath('//a[@class="next i-next"]/@href').get()
        if next_page and next_page !='#' :
            url=next_page
            yield scrapy.Request(url, callback=self.get_Product_urls)

    def parseItem(self,response):
        li={}
        li['URL']=response.request.url
        li['Name']=response.xpath('//h2/text()').get().strip()
        li['SKU']=response.xpath('//div[@class="product-sku"]/text()').get().split('|')[1].strip()
        li['Category']=response.xpath('//div[@class="product-sku"]/text()').get().split('|')[0].strip()
        li['Description']=replace_escape_chars(' '.join(response.xpath('//div[@class="std"]/text()').extract())).strip()
        li['Brand']= 'Furniture of America'
        li['breadcrumbs']=[replace_escape_chars(item) for item in response.xpath('//nav[@class="breadcrumbs"]/ul/li/a/text()').extract()]
        li['breadcrumbs'].append(li['Name'])
        li['Features']='| '.join([replace_escape_chars(item) for item in response.xpath('//ul[@class="simple" or @class="configurable"]/li/text()').extract()])
        specifications={}
        for item in response.xpath('//div[@class="product-dimensions-first"]/ul/li'):
            key=item.xpath('./div[1]/text()').get()
            value=item.xpath('./div[2]/text()').get()
            if(key!=None and value !=None):
                    specifications[key.strip()]=value.strip()

        for item in response.xpath('//div[@class="product-dimensions"]/ul/li'):
            key=item.xpath('./b/text()').get()
            value=item.xpath('./text()').get()
            if(key!=None and value !=None):
                    specifications[key.strip()]=value.strip()

        li.update(specifications)
        li['Documents']=', '.join([link for link in response.xpath('//div[@class="product-dimensions product-download"]/ul/li/a/@href').extract()])

        
        li["image_urls"]=[]
        try:
            for image in response.xpath('//a[@rel="iblightbox[gallery]"]/@href').extract():
                temp={}
                temp['Item_Image']=image
                temp['Detailed_Image']=image
                temp['Zoom_Image']=image
                li["image_urls"].append(temp)
        except:
            li["image_urls"]=[]
        
        yield li