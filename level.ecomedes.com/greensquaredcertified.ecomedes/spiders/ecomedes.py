import scrapy, sys
from scrapy.http import Request


class EcomedesSpider(scrapy.Spider):
    name = 'ecomedes'
    allowed_domains = ['greensquaredcertified.ecomedes.com']
    start_urls = ['https://greensquaredcertified.ecomedes.com/?epd-kind=All']

    print(start_urls)
    sys.exit()

    def parse(self, response):
        product_urls=response.xpath('//*[@class="col-sm-4"]/div/a/@href').extract()

        for product_url in product_urls:
            abs_product_url='https://greensquaredcertified.ecomedes.com'+product_url

            yield Request (abs_product_url,callback=self.parseproduct)

        page=response.xpath('//*[@class="pagination"]')
        current_page=page.xpath('//*[@class="active"]/a/text()').extract()[-1]
        resultscount=response.xpath('//*[@id="meta-description"]/@content').extract_first().split(' ')[0].replace(',','')
        pages=int(resultscount)//18
        if int(current_page) <=pages:
                next_page_url='https://greensquaredcertified.ecomedes.com/?epd-kind=All&page='+str(current_page)
                yield Request (next_page_url,callback=self.parse)



    def parseproduct(self, response):
        general_info={}
        tablediv=response.xpath('//*[@class="list-unstyled product-lenses"]')
        tabledatas=tablediv.xpath('//tbody/tr')
        for tabledata in tabledatas:
            key,value=tabledata.xpath('.//td')
            name=key.xpath('.//text()').extract_first()
            if name == 'Product Page':
                values=value.xpath('.//@href').extract()
                values=list(set(values))
            else:
                values=value.xpath('.//text()').extract()
                
            if len(values) >1:
                values.remove(' ')
                values= ','.join(values)
            else:
            
                values=values[0]
            
            general_info[name]=values
        try:
            contact_email=general_info['Contact Email']
        except:
            contact_email=''
        try:
            contact_name=general_info['Contact Name']
        except:
            contact_name=''
        try:
            contact_phone=general_info['Contact Phone']
        except:
            contact_phone=''
        try:
            product_page=general_info['Product Page']
        except:
            product_page=''
        try:
            certificatename=''
            for c in general_info.keys():
                
                if 'Certificate Number and Link to Document' in c:

                    certificatename=c
            certificate=general_info[certificatename]
        except:
            certificate=''
        try:
            links=response.xpath('//*[contains(text(),"Link to Document")]//parent::td/following-sibling::td')
            document_link=links.xpath('.//@href').extract_first()
        except:
            document_link=''

        Category=response.xpath('.//*[text() = "Category"]/following::dd/span/text()').extract_first()
        subcategory=response.xpath('.//*[text() = "Subcategory"]/following::dd/span/text()').extract_first()
        description=response.xpath('//*[@class="description"]/text()').extract_first()
        compnay_name=response.xpath('.//h3/text()').extract_first()
        series=response.xpath('//*[@class="product-name-title"]/text()').extract_first().strip()

        yield {
            "URL":response.url,
            'Compnay Name':compnay_name,
            'Series':series,
            'Category':Category,
            'Sub Category':subcategory,
            'Description':description,
            "Contact Email":contact_email,
            "Contact Name":contact_name,
            "Contact Phone":contact_phone,
            'Product page':product_page,
            "BIFMA LEVEL Certificate Number ":certificate,
            "LEVEL Certification":document_link

            }
    
    
