from flask import Flask, render_template
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

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
