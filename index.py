import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

app = Flask(__name__)
app.config.from_object(__name__) # load config from this file
app.config.update(dict(
	# DATABASE=os.path.join(app.root_path, 'talk.db'),
	DATABASE='/tmp/talk.db',
	SECRET_KEY='dev key',
	USERNAME='admin',
	PASSWORD='secret'
))
# for env-specific config files:
app.config.from_envvar('TALK_SETTINGS', silent=True)
# The silent switch just tells Flask to not complain if no such environment key is set.

def connect_db():
	db = sqlite3.connect(app.config['DATABASE'])
	db.row_factory = sqlite3.Row
	return db

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def show_messages():
	db = get_db()
	cursor = db.execute('select sender, receiver, message from messages order by id desc')
	messages = cursor.fetchall()
	# username = request.cookies.get('username') or 'stranger'
	return render_template('hello.html', messages=messages)

@app.route('/send/<to>/<message>', methods=['GET','POST'])
def send_message(to, message):
	db = get_db()
	db.execute('insert into messages (sender, receiver, message) values (?, ?, ?)',
		["Esz", to, message])
	db.commit()
	return redirect(url_for('show_messages'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
	app.run()
