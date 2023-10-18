from urllib.request import Request
import scrapy, time
from scrapy.http import Request

class EuropaEuSpider(scrapy.Spider):
    name = 'europa'
    allowed_domains = ['ec.europa.eu']
    start_urls = ['http://ec.europa.eu/ecat/']

    def parse(self, response):
        category_urls=[]
        categorys=response.xpath('//*[@class="panel-body"]')
        for category in categorys:
            url=category.xpath('.//a/@href').extract()
            category_urls=category_urls+url
            
        for category_url in category_urls:
            abs_url='http://ec.europa.eu'+category_url
            print(abs_url)

            yield Request(abs_url,callback=self.parsecat)

    def parsecat(self,response):
        subcates=response.xpath('//tbody/tr/@onclick').extract()
        for sc in subcates:
            try:
                sc_url=sc.split('(')[-1].split(')')[0].replace("'","")
                abs_sc_url='http://ec.europa.eu'+sc_url
                # time.sleep(2)
            except Exception as e:
                print("Error in parsecat ==: ",e)    
            yield Request(abs_sc_url,callback=self.parsecat1)


    def parsecat1(self,response):
        subcates1=response.xpath('//tbody/tr/@onclick').extract()
        for sc in subcates1:
            try:
                sc_url=sc.split('(')[-1].split(')')[0].replace("'","")
                abs_sc_url='http://ec.europa.eu'+sc_url
                # time.sleep(4)
            except Exception as e:
                print("Error in ParseCat1 ==: ",e)
            
            yield Request(abs_sc_url,callback=self.parseproduct)

    def parseproduct(self,response):
        details=response.xpath('//*[@class="list-group productdetails"]/li')
        product_details={}
        for dt in details:
            pd=dt.xpath('.//strong/text()|.//span/@title').extract()
            product_details[pd[0].strip()]=pd[-1].strip()

        print("*"*50)
        print(product_details)
        print("*"*50)
        try:
            
            Licence_No=product_details['Ecolabel Licence No.']

        except:
            Licence_No=''

        try:
            Country=product_details['Country']

        except:
            Country=''
            
        try:
            Company=product_details['Company']

        except:
            Company=''
            
        try:
            Address=product_details['Address']
        except:
            Address=''
            
        try:
            Phone=product_details['Phone']

        except:
            Phone=''
            
        try:
            Website=product_details['Website']

        except:
            Website=''

        try:
            label=response.xpath('//*[@class="insidetitle"]/text()').extract_first().replace('\xa0/','').strip()
        except:
            label=''
        category=response.xpath('//*[@class="insidetitle"]/a/text()').extract_first().strip()
        try:
            description=response.xpath('//*[@id="EN_descriptionText"]/p/text()').extract_first().strip()
        except:
            description=''

        countries=response.xpath('.//*[contains(text(),"EU countries:")]/following-sibling::text()').extract_first()
        title=response.xpath('//h1[@class="media-heading"]/text()').extract_first()

        yield {
            'URL':response.url,
            'Title':title,
            'Label':label,
            'Category':category,
            'Description':description,
            'Licence_No':Licence_No,
            'Country':Country,
            'Company':Company,
            'Address':Address,
            'Phone':Phone,
            'Website':Website,
            'Countries':countries  
        }
                

    