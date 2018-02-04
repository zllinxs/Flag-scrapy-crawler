# -*- coding: utf-8 -*-
import scrapy
import re
from Flag.items import FlagItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FlagSpider(scrapy.Spider):
    name = 'flagspider123'
    allowed_domains = ['example.webscraping.com']

    def start_requests(self):
        for i in range(26):
            url = 'http://example.webscraping.com/places/default/index/' + str(i)
            yield scrapy.Request(url, callback = self.parse)


    #　对已爬下的数据的item检查是否需要，若需要，交给ici
    def parse(self, response):
        for raw_dict in self.construct_raw_dict(response):
            ici = FlagItem()
            for field in ici.fields.keys():
                try:
                    if field in map(str, raw_dict.keys()):
                        ici[field] = raw_dict[field]
                    else:
                        ici[field] = None
                except KeyError:
                    ici[field] = None
            yield ici

    def construct_raw_dict(self, response):  
        # 设置需要爬取的item     
        body_fields = ['flag', 'nation']

        # 根据item爬下对应的数据
        for tbody in response.xpath('//*[@id="results"]/table'):
            #tbody = tbody.xpath('tr')
      
            flag_values = tbody.xpath('./tr/td/div/a/img').extract() # item[flag] 为下载图片的链接
            nation_values = tbody.xpath('./tr/td/div/a/text()').extract() #//*[@id="results"]/table/tbody/tr[1]/td[1]/div/a/text()

            for i in range(len(flag_values)):
            	body_values = []
                body_values.append(re.findall(r'\"(.*)\"', flag_values[i])[0])
                body_values.append(nation_values[i].strip())
        
                yield dict(zip(body_fields, body_values))

