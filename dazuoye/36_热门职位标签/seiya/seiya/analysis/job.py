import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from io import BytesIO
from sqlalchemy import func, desc, and_
from functools import reduce
from ..db import session, engine, Job

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
    for i in l:  # 同上，每个 i 都是字典
        i['salary'] = float(format(i['salary'], '.1f'))
    return l
    
def _hot_tags():
    df = pd.read_sql('select tags from job', engine)
    l = [df.tags[i].split() for i in range(len(df))]
    haha = pd.DataFrame(reduce(lambda a, b: a+b, l), columns=['tags'])
    # 返回值是 Series
    return haha.groupby('tags').size().sort_values(ascending=False).head(10)

def hot_tags():
    # 同上，列表里每个元素都是字典
    return [{'tag': i[0], 'count': i[1]} for i in _hot_tags().items()]

def hot_tags_plot(format='png'):
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
    mpl.rcParams['axes.unicode_minus'] = False  
    mpl.rcParams['figure.figsize'] = 8, 4  # 设置画布宽高，单位英寸
    myfont = mpl.font_manager.FontProperties(
        fname = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
    )
    s = _hot_tags()
    plt.bar(s.index, s.values, color='green')
    plt.title(u'热门职位标签', fontproperties=myfont)
    img = BytesIO()  # 开启进入内存空间之门
    plt.savefig(img, format=format)  # 把整个图的数据放到内存中
    return img.getvalue()

def experience_stats():
    query = session.query(
        Job.experience, 
        func.count(Job.experience).label('count')
    ).group_by('experience').order_by(desc('count'))
    l = [i._asdict() for i in query]
    z = sum([i['count'] for i in l])
    for i in l:
        i['percent'] = float(format(i['count'] / z, '.3f'))
    l[-1]['percent'] = (1000 - 1000 * sum([i['percent'] for i in l[:-1]]))/1000
    return l

def education_stats():
    query = session.query(
        Job.education, 
        func.count(Job.education).label('count')
    ).group_by('education').order_by(desc('count'))
    return [i._asdict() for i in query]

