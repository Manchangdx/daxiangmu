import os, json, sys
from faker import Faker
from random import randint
from jobplus.models import db, User, CompanyDetail, Job
from manage import app

app.app_context().push()

fake = Faker('zh-cn')

with open(os.path.join(os.path.dirname(__file__), 'data_company.json')) as f:
    data_company = json.load(f)

with open(os.path.join(os.path.dirname(__file__), 'data_job.json')) as f:
    data_job = json.load(f)

def iter_user():
    for i in data_company:
        yield User(
            name=i['name'],
            email=fake.email(),
            password=fake.password(),
            role=22
        )

l = list(iter_user())

def iter_companydetail():
    for u, d in zip(l, data_company):
        yield CompanyDetail(
            user=u,
            image_url=d['image_url'],
            finance=d['finance'],
            staff_num=d['staff_num'],
            type=d['type'],
            about=d['about']
        )

def iter_job():
    for i, u in enumerate(l):
        n = randint(2, 5)
        while n > 0:
            d = data_job[n+i*5-1]
            yield Job(
                user = u,
                name=d['name'],
                salary=d['salary'],
                location=d['location'],
                experience_requirement=d['experience_requirement'],
                degree_requirement=d['degree_requirement'],
                release_time=d['release_time']
            )
            n -= 1

def run():
    for i in l:
        db.session.add(i)
    for i in iter_companydetail():
        db.session.add(i)
    for i in iter_job():
        db.session.add(i)
    db.session.commit()


if __name__ == '__main__':
    run()