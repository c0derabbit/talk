import sqlite3
from datetime import datetime as time
from flask import Flask, request, session, g, redirect, url_for, \
	render_template, flash
from flask_moment import Moment
from utils import *
from config import *


app = Flask(__name__)
app.config.update(dev_env)

moment = Moment(app)

def connect_db():
	db = sqlite3.connect(app.config['DATABASE'])
	db.row_factory = sqlite3.Row
	return db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

from views import *

if __name__ == '__main__':
	with app.app_context():
		app.run()
