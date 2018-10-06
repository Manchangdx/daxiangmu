from flask import Flask, render_template, Response
import seiya.analysis.job as job

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/g2')
def g2():
    return render_template('g2.html')

@app.route('/job')
def job_index():
    return render_template('job/index.html')

@app.route('/job/count_top10')
def job_count_top10():
    return render_template('job/count_top10.html', query=job.count_top10())

@app.route('/job/salary_top10')
def job_salary_top10():
    return render_template('job/salary_top10.html', query=job.salary_top10())

@app.route('/job/hot_tags')
def job_hot_tags():
    return render_template('job/hot_tags.html', query=job.hot_tags())

@app.route('/job/hot_tags.png')
def job_hot_tags_plot():
    # Response 是将数据直接发送给浏览器，不需要前端模板了
    # 这里就是将一张图的数据直接发送给浏览器
    return Response(job.hot_tags_plot(), content_type='image/png')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
