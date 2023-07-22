# app/__init__.py

from flask import Flask
from app.db import connect

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['DB_CONN'] = connect()

from app.views.company_views import company_bp
from app.views.job_views import job_bp
from app.views.home_views import home_bp

app.register_blueprint(company_bp, url_prefix='/companies')
app.register_blueprint(job_bp, url_prefix='/jobs')
app.register_blueprint(home_bp, url_prefix='')  # Use an empty string for root

