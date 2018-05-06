import scrapy
from functools import reduce

class Company_spider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://www.zhipin.com/?ka=header-home']

    def parse(self, response):
        for i in response.css('div.common-tab-box ul.cur')[1].css('li'):
            url = i.css('a::attr(href)').extract_first()
            request = scrapy.Request('https://www.zhipin.com'+url, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        yield {
            'name': response.css('h1.name::text').extract_first(),
            'image_url': response.css('div.company-logo img::attr(src)').extract_first(),
            'finance': response.css('div.info-primary p::text').extract()[0],
            'type': response.css('div.info-primary p::text').extract()[2],
            'staff_num': response.css('div.info-primary p::text').extract()[1],
            'about': reduce(lambda a, b: a.strip()+b.strip(), response.css('div.detail-content div.text::text').extract())
            }
