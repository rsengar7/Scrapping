# https://www.sedar.com/FindCompanyDocuments.do?lang=EN&page_no=1&company_search=All+%28or+type+a+name%29&document_selection=0&industry_group=A&FromDate=15&FromMonth=01&FromYear=1997&ToDate=15&ToMonth=07&ToYear=2022&Variable=Issuer

import scrapy
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import re
from scrapy.http.request import Request


class SedarSpider(scrapy.Spider):
    name = 'sedar'
    allowed_domains = ['sedar.com']
    max_retries = 2
    # Done
    # 'https://www.sedar.com/FindCompanyDocuments.do?lang=EN&page_no=1&company_search=All+%28or+type+a+name%29&document_selection=0&industry_group=A&FromDate=15&FromMonth=01&FromYear=1997&ToDate=15&ToMonth=01&ToYear=1998&Variable=Issuer'
    # start_urls = ['https://www.sedar.com/FindCompanyDocuments.do?lang=EN&page_no=1&company_search=All+%28or+type+a+name%29&document_selection=0&industry_group=A&FromDate=15&FromMonth=01&FromYear=1997&ToDate=26&ToMonth=07&ToYear=2022&Variable=Issuer']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retries = {}

    def start_requests(self):
        yield Request(
        
            'https://sedar.com/FindCompanyDocuments.do?lang=EN&page_no=1&company_search=All+%28or+type+a+name%29&document_selection=0&industry_group=A&FromDate=16&FromMonth=12&FromYear=1999&ToDate=31&ToMonth=12&ToYear=1999&Variable=Issuer',
            callback = self.parse,
            meta = {
                'handle_httpstatus_list': [302],
            },
        )
    
    def parse(self, response):
        for item in response.xpath('//table[@align="center"]//tr'):
            li={}
            try:
                li['Company Name']=item.xpath('./td[1]/a/text()').get().strip()
                li['Company URL']='https://www.sedar.com'+item.xpath('./td[1]/a/@href').get()
                li['Date of Filling']=item.xpath('./td[2]/text()').get().strip()
                li['Time of Filling']=item.xpath('./td[3]/text()').get().strip()
                li['Document Type']=item.xpath('./td[4]/form/p/a/text()').get().strip()
                li['Docuement URL']='https://www.sedar.com'+item.xpath('./td[4]/form/@action').get()
                li['File Type']=item.xpath('./td[5]/text()').get().strip()
                li['File Size']=re.sub('\\xa0','',item.xpath('./td[6]/text()').get().strip())
            except:
                continue
            yield li

        nextPage=response.xpath('////*[@src="/images/searchnext.gif"]/parent::a/@href').get()
        if nextPage:
            nextPage='https://www.sedar.com'+nextPage
            yield scrapy.Request(nextPage,callback=self.parse)

