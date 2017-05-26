from datetime import datetime as time
from flask import Flask, request, session, redirect, url_for, \
	render_template, flash
from talk import app, get_db
from decorators import *
from utils import *
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

p = PasswordHasher(hash_len=256,salt_len=256)


@app.route('/')
@login_required
def show_messages():
	db = get_db()
	cursor = db.execute('select sender, receiver, sent_at, message from messages order by id desc')
	messages = cursor.fetchall()
	messages = [{'sender': m[0], 'receiver': m[1], 'sent_at': parse_date(m[2]), 'message': m[3]} for m in messages]
	session['partner'] = 'Samu' if session.get('username') == 'eszter' else 'Eszter'
	return render_template('messages.html', messages=messages, partner=session.get('partner'))


@app.route('/send', methods=['POST'])
@login_required
def send_message():
	db = get_db()
	current_datetime = stringify_date(time.utcnow())
	db.execute('insert into messages (sender, receiver, sent_at, message) values (?, ?, ?, ?)',
		[session.get('username'), session.get('partner'), current_datetime, request.form['message']])
	db.commit()
	return redirect(url_for('show_messages'))


@app.route('/login', methods=['GET', 'POST'])
@only_show_if_not_logged_in
def login():
	error = None
	if request.method == 'POST':
		db = get_db()
		cursor = db.execute('select username, password from users where username is (?)',
			[request.form['username']])
		user = cursor.fetchone()
		if user is not None:
			try:
				p.verify(user['password'], request.form['password'])
				session['logged_in'] = True
				session['username'] = request.form['username']
				return redirect(url_for('show_messages'))
			except VerificationError:
				error = 'Incorrect username or password'
		error = 'Incorrect username or password'
	return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
@only_show_if_not_logged_in
def signup():
	error = None
	if session.get('logged_in'):
		flash('You are already logged in as {}'.format(session.get('username')))
		return redirect(url_for('show_messages'))
	if request.method == 'POST':
		if request.form['passwordCheck'] != '' and request.form['password'] != request.form['passwordCheck']:
			error = 'Passwords don\'t match'
		else:
			db = get_db()
			# TODO check if username already exists
			db.execute('insert into users (username, password) values (?, ?)',
				[request.form['username'], p.hash(request.form['password'])])
			db.commit()
			flash('You registered successfully. Welcome to the club!')
			return redirect(url_for('login'))
	return render_template('signup.html', error=error)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
