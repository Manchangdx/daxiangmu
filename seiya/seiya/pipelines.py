import re
from sqlalchemy.orm import sessionmaker
from .job import engine, JobModel
from .items import JobItem

class SeiyaPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JobItem):
            return self._process_jobitem(item)

    #def _process_jobitem(self, item, spider):
    def _process_jobitem(self, item):
        l, u = 0, 0
        s = re.findall('(\d+)k-(\d+)k', item['salary'])
        if s:
            l, u = s[0]
        experience, education = re.findall('经验(.+) / (.+)', item['exp_edu'])[0]
        data = JobModel(
            title = item['title'],
            city = item['city'],
            salary_lower = int(l),
            salary_upper = int(u),
            experience = experience,
            education = education,
            tags = item['tags'].split('/')[0].strip().replace(',', ' '),
            company = item['company']
        )
        print('-------------------')
        print(data)
        self.session.add(data)

    def open_spider(self, spider):
        self.session = sessionmaker(engine)()

    def close_spider(self, spider):
        self.session.commit()
        sefl.session.close()
