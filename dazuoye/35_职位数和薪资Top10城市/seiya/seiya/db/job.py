from sqlalchemy import Column, String, Integer
from .base import Base, engine


class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    title = Column(String(64), index=True)
    city = Column(String(16), index=True)
    salary_lower = Column(Integer)
    salary_upper = Column(Integer)
#experience_lower = Column(Integer)
#experience_upper = Column(Integer)
    experience = Column(String(32))
    education = Column(String(16))
    tags = Column(String(256))
    company = Column(String(32))

#Base.metadata.create_all()

'''
if __name__ == '__main__':
    Base.metadata.create_all()
'''
