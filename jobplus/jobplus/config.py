class BaseConfig:
    SECRET_KEY = 'shiyanlou'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    COMPANY_PER_PAGE = 6
    JOB_PER_PAGE = 6
    ADMIN_PER_PAGE = 10

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/jobplus?charset=utf8'

class ProConfig(BaseConfig):
    pass

configs = {
    'dev': DevConfig,
    'pro': ProConfig
}
