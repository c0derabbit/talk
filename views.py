from datetime import datetime as time
from flask import Flask, request, session, redirect, url_for, \
	render_template, flash
from talk import app, get_db
from decorators import *
from utils import *
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

p = PasswordHasher(hash_len=256, salt_len=256)


@app.route('/')
@login_required
def dashboard():
	cur = get_db().cursor()
	cur.execute("select username from users where username!='{}'".format(session.get('username')))
	users = cur.fetchall()
	users = [u[0] for u in users]
	return render_template('dashboard.html', users=users)


@app.route('/messages/<partner>')
@login_required
def show_messages(partner):
	session['partner'] = partner
	cur = get_db().cursor()
	cur.execute("select sender, receiver, sent_at, message from messages\
	 	where (sender='{0}' and receiver='{1}')\
		or (sender='{1}' and receiver='{0}')\
		order by id desc".format(session.get('username'), session.get('partner')))
	messages = cur.fetchall()
	messages = [{'sender': m[0], 'receiver': m[1], 'sent_at': parse_date(m[2]), 'message': m[3]} for m in messages]
	return render_template('messages.html', messages=messages, partner=partner)


@app.route('/send', methods=['POST'])
@login_required
def send_message():
	conn = get_db()
	cur = conn.cursor()
	current_datetime = stringify_date(time.utcnow())
	cur.execute('insert into messages (sender, receiver, sent_at, message) values (%s, %s, %s, %s);',
		(session.get('username'), session.get('partner'), current_datetime, request.form['message']))
	conn.commit()
	return redirect(url_for('show_messages', partner=session.get('partner')))


@app.route('/login', methods=['GET', 'POST'])
@only_show_if_not_logged_in
def login():
	error = None
	if request.method == 'POST':
		cur = get_db().cursor()
		cur.execute("select username, password from users where username='{}'".format(request.form['username']))
		user_props = cur.fetchone()
		if user_props is not None:
			password = str(user_props[1])
			try:
				p.verify(password, request.form['password'])
				session['logged_in'] = True
				session['username'] = request.form['username']
				return redirect(url_for('dashboard'))
			except VerificationError:
				error = 'Incorrect username or password'
		error = 'Incorrect username or password'

	return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	session.pop('username')
	session.pop('partner')
	flash('You were logged out')
	return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
@only_show_if_not_logged_in
def signup():
	error = None
	if request.method == 'POST':
		conn = get_db()
		cur = conn.cursor()
		user = cur.execute("select username from users where username='{}'".format(request.form['username']))
		user_props = cur.fetchone()
		if user_props is not None:
			error = 'This username is already taken. Please choose another one.'
		elif len(request.form['password']) < 8:
			error = 'Your password is too short. It should be at least 8 characters.'
		elif request.form['password'] != request.form['passwordCheck']:
			error = 'Passwords don\'t match'
		else:
			cur.execute("insert into users (username, password) values ('{}', E'{}');".format(
				request.form['username'], p.hash(request.form['password'])))
			conn.commit()
			flash('You registered successfully. Welcome to the club!')
			return redirect(url_for('login'))

	return render_template('signup.html', error=error)


@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def change_pw():
	error = None
	if request.method == 'POST':
		db = get_db()
		cursor = db.execute('select username, password from users where username is (?)',
			[session.get('username')])
		user = cursor.fetchone()

		try:
			p.verify(user['password'], request.form['old_password'])
			if len(request.form['new_password']) < 8:
				error = 'Your new password is too short. It should be at least 8 characters.'
			elif request.form['new_password'] != request.form['new_password_check']:
				error = 'Your new passwords don\'t match'
			else:
				db.execute('update users set password = (%s) where username is (%s)',
					(p.hash(request.form['new_password']), session.get('username')))
				db.commit()
				flash('Password updated, you are good to go.')

				return redirect(url_for('dashboard'))

		except VerificationError:
			error = 'Your old password is incorrect'

	return render_template('changepassword.html', error=error)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
