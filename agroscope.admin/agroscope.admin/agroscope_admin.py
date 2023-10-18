from ntpath import join
import scrapy


class AgroscopeAdminSpider(scrapy.Spider):
    name = 'agroscope.admin'
    allowed_domains = ['agroscope.admin.ch']
    start_urls = ['https://www.agroscope.admin.ch/agroscope/en/home/topics/environment-resources/life-cycle-assessment/life-cycle-assessment-applications.html','https://www.agroscope.admin.ch/agroscope/en/home/topics/environment-resources/life-cycle-assessment/life-cycle-assessment-databases.html','https://www.agroscope.admin.ch/agroscope/en/home/topics/environment-resources/life-cycle-assessment/life-cycle-assessment-methods.html']


    def parse(self, response):
        # print(response.text)
        urls=response.xpath('//h3/a/@href').extract()
        # print(urls,len(urls))
        if urls:
            for url in urls:
                url='https://www.agroscope.admin.ch'+url
                yield scrapy.Request(url,callback=self.parse)

        else:
            li={}
            li['url']=response.url
            li['title']=response.xpath('//h1/text()').get()
            li['description']='  '.join([item.strip() for item in response.xpath('//article[@class="clearfix"]//text()').extract() if item.strip() != ''])
            li['downloads']=', '.join(['https://www.agroscope.admin.ch'+item for item in response.xpath('//a[@class="icon icon--before icon--pdf"]/@href').extract()]) 

            li['websites']=', '.join([item for item in response.xpath('//a[@class="icon icon--after icon--external"]/@href').extract() if 'http' in item])
            li['other resources']=', '.join(['https://www.agroscope.admin.ch'+item for item in response.xpath('//div[@class="mod mod-link"]/p/a/@href').extract() if 'http' not in item])
            yield li

