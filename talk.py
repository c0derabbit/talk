import sqlite3
import psycopg2 # postgresql
import urlparse
from datetime import datetime as time
from flask import Flask, request, session, g, redirect, url_for, \
	render_template, flash
from flask_moment import Moment
from utils import *
from config import *


app = Flask(__name__)
app.config.update(prod_env)

moment = Moment(app)

urlparse.uses_netloc.append('postgres')
db_url = urlparse.urlparse(app.config['DATABASE_URL'])

def get_db():
	conn = psycopg2.connect(
		database=db_url.path[1:],
		user=db_url.username,
		password=db_url.password,
		host=db_url.hostname,
		port=db_url.port
	)
	return conn

@app.teardown_appcontext
def close_db(error):
	get_db().close()

from views import *

if __name__ == '__main__':
	with app.app_context():
		app.run()
