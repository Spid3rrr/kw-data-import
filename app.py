from flask import Flask
import upload_files

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'This is a cron job script for SuperStack'

@app.route('/alive')
def alive():
    return 'alive'

@app.route('/upload_properties')
def upload_properties():
    return upload_files.upload_properties()

@app.route('/upload_sales')
def upload_sales():
    return upload_files.upload_sales()

@app.route('/upload_skipper_stats_sales')
def upload_skipper_stats_sales():
    return upload_files.upload_skipper_stats_sales()