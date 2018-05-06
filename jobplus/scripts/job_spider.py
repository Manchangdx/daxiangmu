import scrapy

class JobSpider(scrapy.Spider):
    name = 'job'
    start_urls = ['https://www.zhipin.com/c101010100/?page={haha}&ka=page-{haha}'.format(haha=i) for i in range(1, 4)]

    def parse(self, response):
       for i in response.css('div.job-primary'): 
            yield {
                'name': i.css('div.job-title::text').extract_first(),
                'salary': i.css('span::text').extract_first(),
                'location': i.css('p::text').extract()[0],
                'experience_requirement': i.css('p::text').extract()[1],
                'degree_requirement': i.css('p::text').extract()[2],
                'release_time': i.css('div.info-publis p::text').extract_first()
            }
