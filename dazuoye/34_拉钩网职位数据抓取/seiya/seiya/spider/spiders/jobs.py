import scrapy
from ..items import JobItem

class JobSpider(scrapy.Spider):
    name = 'jobs'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
    }

    def start_requests(self):
        urls = ['https://www.lagou.com/zhaopin/{}/?filterOption=2'.format(i) for i in range(1, 31)]
        for i in urls:
            yield scrapy.Request(url=i, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for i in response.css('li.con_list_item.default_list'):
            yield JobItem({
                'title': i.css('h3::text').extract_first(),
                'city': i.css('em::text').extract_first(),
                'salary': i.css('span.money::text').extract_first(),
                'exp_edu': i.css('div.li_b_l::text').extract()[2].strip(),
                'tags': i.css('div.industry::text').extract_first(),
                'company': i.css('div.company_name a::text').extract_first()
            })
