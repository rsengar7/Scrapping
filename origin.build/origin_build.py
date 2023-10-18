from ntpath import join
import scrapy
import re
from w3lib.html import remove_tags, replace_entities, replace_escape_chars

class OriginBuildSpider(scrapy.Spider):
    name = 'origin.build'
    allowed_domains = ['origin.build']
    try:
        with open('origin.build-materialIDs.csv') as f:
            start_urls = f.readlines()
    except:
        pass
    start_urls = ['https://origin.build/equinox/api/public/companies/random?size=100&companyTypes=MANUFACTURER&packageTypes=MANUFACTURER_ENHANCED,MANUFACTURER_NEXT,MANUFACTURER_ENHANCED_PLUS,MANUFACTURER_ADVANCED,MANUFACTURER_PRO&locale=en&xreqts=1657454115752']
    # start_urls = ['https://origin.build/equinox/api/public/materials/100233791?locale=en&webtrxid=YsqxuTe4ahucB0iUWLohbgAAABg&srid=null&xreqts=1657451231669','https://origin.build/equinox/api/public/materials/100315033?locale=en&webtrxid=YsqxuTe4ahucB0iUWLohbgAAABg&srid=null&xreqts=1657451295645','https://origin.build/equinox/api/public/materials/100211962?locale=en&webtrxid=YsqxuTe4ahucB0iUWLohbgAAABg&srid=null&xreqts=1657451295645']
    
    # def start_requests(self):
    #     if not self.start_urls and hasattr(self, 'start_url'):
    #         raise AttributeError(
    #             "Crawling could not start: 'start_urls' not found "
    #             "or empty (but found 'start_url' attribute instead, "
    #             "did you miss an 's'?)")
    #     for material_id in self.start_urls[3000:3750]:
    #         material_url="https://origin.build/equinox/api/public/materials/"+material_id.strip()+"?locale=en&webtrxid=YsqxuTe4ahucB0iUWLohbgAAABg&srid=null&xreqts=1657451295645"
    #         yield scrapy.Request(material_url,callback=self.parseMaterial)

    
    
    def parse(self, response):
        response_json = response.json()
        for item in response_json['http://giga.build/schema/page']:
            brand_id=item["http://giga.build/schema/id"]
            brand_url="https://origin.build/equinox/api/public/materials/facet?locale=en&vlevel=P&companybrandid=C"+brand_id+"&view=full&page=0&size=25&tuid=3cdd669f-24af-4e8a-a074-60ff414fb569&xreqts=1657451044480"
            yield scrapy.Request(brand_url, callback=self.parseBrand)

   
    def parseBrand(self, response):
        response_json = response.json()
        for item in response_json['http://giga.build/schema/page']:
            material_id=item["http://giga.build/schema/id"]
            print(material_id)
            material_url="https://origin.build/equinox/api/public/materials/"+material_id+"?locale=en&webtrxid=YsqxuTe4ahucB0iUWLohbgAAABg&srid=null&xreqts=1657451295645"
            # yield {'material_id':material_id}
            yield scrapy.Request(material_url, callback=self.parseMaterial)

        current_page=response_json['http://giga.build/schema/currentpage']
        total_page=response_json['http://giga.build/schema/totalpages']
        if current_page<total_page-1:
            next_page_str=str(current_page+1)
            next_page_url=re.sub(r'page=\d+', 'page='+next_page_str, response.url)
            yield scrapy.Request(next_page_url, callback=self.parseBrand)
        

    def parseMaterial(self, response):
        response_json = response.json()
        li={}
        id=response.url.split('/')[-1].split('?')[0]
        li['URL']='https://origin.build/#/material/'+id
        li['Name']=response_json['http://schema.org/name']

        try:
            li['Description']=replace_escape_chars(remove_tags(response_json.get('http://schema.org/description')))
        except:
            li['Description']=''

        li['Org URL']=response_json.get('http://schema.org/url')
        try:
            li['CSI Category']=response_json["http://giga.build/schema/csicategory"].get("http://schema.org/name")
        except:
            li['CSI Category']=None

        li['Company ID']=response_json.get("http://giga.build/schema/decoratedContextId")
        li['Company Page']='https://origin.build/#/company/'+li['Company ID']+'?locale=en&selectedTab=contact'
        try:
            li['Category']=response_json["http://giga.build/schema/category"].get("http://schema.org/name")
        except:
            try:
                li['Category']=''.join(response_json["http://giga.build/schema/category"])
            except:
                li['Category']=None
        try:
            li['Collection']=response_json["http://giga.build/schema/serie"].get("http://schema.org/name")
        except:
            li['Collection']=None
        try:
            li['Library']=response_json["http://giga.build/schema/events"].get("http://schema.org/name")
            li['Library URL']=response_json["http://giga.build/schema/events"].get("http://schema.org/url")
        except:
            li['Library']=None
            li['Library URL']=None

        certifications=[]
        try:
            for item in response_json["http://giga.build/schema/certification"]:
                certificate={}
                certificate['Program Name']=item["http://giga.build/schema/standard"].get("http://schema.org/name")
                certificate['Reporting Body']=item["http://giga.build/schema/source"].get("http://schema.org/name")
                try:
                    certificate['Document No']=item["http://giga.build/schema/decorationEntity"].get("http://giga.build/schema/certificationNumber")
                except:
                    certificate['Document No']=None
                try:
                    certificate['Expiry Date']=item["http://giga.build/schema/endDate"]
                except:
                    certificate['Expiry Date']=None
                try:
                    certificate['Supporting Docs']=item["http://schema.org/url"]
                except:
                    certificate['Supporting Docs']=None

                Additional_Info={}
                try:
                    for info in item['http://giga.build/schema/options']:
                        key=info["http://schema.org/name"]
                        value=info["http://schema.org/value"]
                        Additional_Info[key]=value
                        certificate['Additional Info']=Additional_Info
                except:
                    try:
                        key=item['http://giga.build/schema/options']["http://schema.org/name"]
                        value=item['http://giga.build/schema/options']["http://schema.org/value"]
                        Additional_Info[key]=value
                        certificate['Additional Info']=Additional_Info
                    except:
                        certificate['Additional Info']=None
                certifications.append(certificate)

        except:
            try:
                item=response_json["http://giga.build/schema/certification"]
                certificate={}
                certificate['Program Name']=item["http://giga.build/schema/standard"].get("http://schema.org/name")
                certificate['Reporting Body']=item["http://giga.build/schema/source"].get("http://schema.org/name")
                try:
                    certificate['Document No']=item["http://giga.build/schema/decorationEntity"].get("http://giga.build/schema/certificationNumber")
                except:
                    certificate['Document No']=None
                try:
                    certificate['Expiry Date']=item["http://giga.build/schema/endDate"]
                except:
                    certificate['Expiry Date']=None
                try:
                    certificate['Supporting Docs']=item["http://schema.org/url"]
                except:
                    certificate['Supporting Docs']=None

                Additional_Info={}
                try:
                    for info in item['http://giga.build/schema/options']:
                        key=info["http://schema.org/name"]
                        value=info["http://schema.org/value"]
                        Additional_Info[key]=value
                        certificate['Additional Info']=Additional_Info
                except:
                    try:
                        key=item['http://giga.build/schema/options']["http://schema.org/name"]
                        value=item['http://giga.build/schema/options']["http://schema.org/value"]
                        Additional_Info[key]=value
                        certificate['Additional Info']=Additional_Info
                    except:
                        certificate['Additional Info']=None
                certifications.append(certificate)
            except:
                pass


        li['Certifications']=certifications
        print("*"*100)
        print(certifications)
        print("*"*100)

        features={}
        try:
            for info in response_json['http://giga.build/schema/options']:
                key=info["http://schema.org/name"]
                value=info["http://schema.org/value"]
                features[key]=value
        except:
            try:
                key=response_json['http://giga.build/schema/options']["http://schema.org/name"]
                value=item['http://giga.build/schema/options']["http://schema.org/value"]
                features[key]=value
            except:
                features={}

        li['Features']=features

        contacts=[]
        try:

            for info in response_json["http://giga.build/schema/service"]:
                contact={}
                try:
                    contact['Name']=info["http://schema.org/provider"]["http://schema.org/contactPoint"]["http://schema.org/name"]
                except KeyError:
                    contact['Name']=None
                try:
                    contact['Email']=info["http://schema.org/provider"]["http://schema.org/contactPoint"]["http://schema.org/email"]
                except:
                    contact['Email']=None
                try:
                    contact['Telephone']=info["http://schema.org/provider"]["http://schema.org/contactPoint"]["http://schema.org/telephone"]
                except:
                    contact['Telephone']=None
                try:
                    contact['Address']=info["http://schema.org/provider"]["http://schema.org/contactPoint"]["http://schema.org/contactOption"]["http://schema.org/description"]
                except:
                    contact['Address']=None
                contacts.append(contact)

        except:
            try:
                contact={}
                contact['Name']=response_json["http://giga.build/schema/service"]["http://schema.org/provider"]["http://schema.org/contactPoint"]["http://schema.org/name"]
                contact['Email']=response_json["http://giga.build/schema/service"]["http://schema.org/provider"]["http://schema.org/contactPoint"]["http://schema.org/email"]
                try:
                    contact['Telephone']=response_json["http://giga.build/schema/service"]["http://schema.org/provider"]["http://schema.org/contactPoint"]["http://schema.org/telephone"]
                except:
                    contact['Telephone']=None
                try:
                    contact['Address']=response_json["http://giga.build/schema/service"]["http://schema.org/provider"]["http://schema.org/contactPoint"]["http://schema.org/contactOption"]["http://schema.org/description"]
                except:
                    contact['Address']=None
            except:
                pass
        contacts.append(contact)

        li['Contacts']=contacts
       

        try:
            li['Tag words']=response_json["http://schema.org/alternateName"]
        except:
            li['Tag words']=None    
        
        
        yield li    
