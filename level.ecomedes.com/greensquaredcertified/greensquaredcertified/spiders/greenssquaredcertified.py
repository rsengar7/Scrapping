import scrapy, sys
from scrapy.http import Request


class EcomedesSpider(scrapy.Spider):
    name = 'greensquaredcertified'
    allowed_domains = ['greensquaredcertified.ecomedes.com']
    start_urls = ['https://greensquaredcertified.ecomedes.com/?epd-kind=All']

    def parse(self, response):
        product_urls=response.xpath('//*[@class="col-sm-4"]/div/a/@href').extract()
        print("*"*50)
        print(product_urls)
        print("*"*50)

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
        print("Response -------> ",response)
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
                print("Values ------------:")
                print(values)
                print("*"*50)
                try:
                    values.remove(' ')
                except: pass
                values= ','.join(values)
            else:
            
                values=values[0]
            
            general_info[name]=values
        try:
            contact_name=general_info['Contact Name']
        except:
            contact_name=''
        try:
            product_page=general_info['Product Page']
        except:
            product_page=''
        #-------------
        try:
            CA_Section_01350 = general_info['CA Section 01350']
        except:
            CA_Section_01350 = ''
        try:
            CDPH_Standard_Method_V1 = general_info['CDPH Standard Method V1.2-2017']
        except:
            CDPH_Standard_Method_V1 = ''
        try:
            Environmental_Product_Declaration = general_info['Environmental Product Declaration (EPD)']
        except:
            Environmental_Product_Declaration = ''
        try:
            Green_Squared_Certificate = general_info['Green Squared Certificate']
        except:
            Green_Squared_Certificate = ''
        try:
            certfied_material_complaint = general_info['LEED PC 112 - Certified Multi-Attribute Products and Materials Compliant']
        except:
            certfied_material_complaint = ''
        try:
            nahb = general_info['NAHB National Green Building Standard - 611.2 Sustainable Products']
        except:
            nahb = ''
        try:
            igcc = general_info['IgCC 2015 - 505.3.2 Multi-Attribute Standard Compliant']
        except:
            igncc = ''
        try:
            UL_GREENGUARD_Certificate = general_info['UL GREENGUARD Certificate']
        except:
            UL_GREENGUARD_Certificate = ''
        try:
            UL_GREENGUARD_GOLD_Certificate = general_info['UL GREENGUARD GOLD Certificate']
        except:
            UL_GREENGUARD_GOLD_Certificate = ''

        try:
            links=response.xpath('//*[contains(text(),"Green Building Codes")]//parent::td/following-sibling::td')
            document_link=links.xpath('.//@href').extract_first()
        except:
            document_link=''
        
        try:
            links=response.xpath('//*[contains(text(),"Tile Lifecycle Cost Comparison")]//parent::td/following-sibling::td')
            lifecycle_cost=links.xpath('.//@href').extract_first()
        except:
            lifecycle_cost=''
        
        try:
            links=response.xpath('//*[contains(text(),"The Natural Choice Informative Brochure")]//parent::td/following-sibling::td')
            information_brochure=links.xpath('.//@href').extract_first()
        except:
            information_brochure=''

        description=response.xpath('//*[@class="description"]/text()').extract_first()
        compnay_name=response.xpath('.//h3/text()').extract_first()
        series=response.xpath('//*[@class="product-name-title"]/text()').extract_first().strip()

        yield {
            "URL":response.url,
            'Compnay Name':compnay_name,
            'Series':series,
            'Description':description,
            "Contact Name":contact_name,
            'Product page':product_page,
            'CA Section 01350': CA_Section_01350,
            'CDPH Standard Method V1.2-2017': CDPH_Standard_Method_V1,
            'Environmental Product Declaration (EPD)': Environmental_Product_Declaration,
            'Green Squared Certificate': Green_Squared_Certificate,
            'LEED PC 112 - Certified Multi-Attribute Products and Materials Compliant': certfied_material_complaint,
            'NAHB National Green Building Standard - 611.2 Sustainable Products': nahb,
            'IgCC 2015 - 505.3.2 Multi-Attribute Standard Compliant': igcc,
            'UL GREENGUARD Certificate': UL_GREENGUARD_Certificate,
            'UL GREENGUARD GOLD Certificate': UL_GREENGUARD_GOLD_Certificate,
            "Green Building Codes, Standards & Rating Systems Guide":document_link,
            "Tile Lifecycle Cost Comparison": lifecycle_cost,
            "The Natural Choice Informative Brochure": information_brochure
            }
    
    
