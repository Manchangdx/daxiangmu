# 选择目录
cd /home/shiyanlou

# 下载压缩包，解压，切换目录
wget https://labfile.oss.aliyuncs.com/courses/8913/jobplus.zip
unzip jobplus.zip
cd jobplus

# 安装依赖库
sudo apt update
sudo apt install -y libmysqlclient-dev
sudo pip install -r requirements.txt

# 启动 MySQL 服务，创建数据库
sudo service mysql start
mysql -uroot -e 'CREATE SCHEMA IF NOT EXISTS jobplus CHARSET = UTF8'

# 设置环境变量
export FLASK_APP=manage.py FLASK_DEBUG=1

# 数据表迁移，创建测试数据
flask db upgrade
python3 -m scripts.generate_data

# 启动项目
flask run
