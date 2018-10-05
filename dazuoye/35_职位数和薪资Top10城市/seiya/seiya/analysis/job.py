from sqlalchemy import func, desc, and_
from ..db import session, Job

def count_top10():
    query = session.query(
        Job.city,  # 城市名儿
        func.count(Job.city).label('count')  # 职位数量
    ).group_by(Job.city).order_by(desc('count')).limit(10)
    return [i._asdict() for i in query]  # 每个 i 是一个字典

def salary_top10():
    query = session.query(
        Job.city, 
        func.avg((Job.salary_lower+Job.salary_upper)/2).label('salary')
    ).filter(
        and_(Job.salary_lower>0, Job.salary_upper>0)
    ).group_by(Job.city).order_by(desc('salary')).limit(10)
    l = [i._asdict() for i in query]
    for i in l:
        i['salary'] = float(format(i['salary'], '.1f'))
    return l
    
