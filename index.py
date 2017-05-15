import os
import sqlite3
from datetime import datetime as d
from flask import Flask, request, session, g, redirect, url_for, \
	render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
	# DATABASE=os.path.join(app.root_path, 'talk.db'),
	DATABASE='/tmp/talk.db',
	SECRET_KEY='dev key',
	USER1='eszter',
	USER2='Samu',
	PASSWORD='secret'
))

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
	try:
		db = get_db()
		cursor = db.execute('select sender, receiver, sent_at, message from messages order by id desc')
		messages = cursor.fetchall()
		session['partner'] = 'Samu' if session['username'] == 'eszter' else 'Eszter'
		return render_template('messages.html', messages=messages, partner=session['partner'])
	except KeyError:
		return redirect(url_for('login'))

@app.route('/send', methods=['POST'])
def send_message():
	db = get_db()
	current_datetime = d.now().strftime('%y.%m.%d %H:%m')
	db.execute('insert into messages (sender, receiver, sent_at, message) values (?, ?, ?, ?)',
		[session['username'], session['partner'], current_datetime, request.form['message']])
	db.commit()
	return redirect(url_for('show_messages'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		# if request.form['username'] != app.config['USER1'] or request.form['username'] != app.config['USER2']:
		# 	error = 'Invalid username'
		if request.form['password'] != app.config['PASSWORD']:
			error = 'Incorrect password'
		else:
			session['logged_in'] = True
			session['username'] = request.form['username']
			return redirect(url_for('show_messages'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
	app.run()
