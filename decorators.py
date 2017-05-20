from flask import request, session, redirect, url_for, flash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def only_show_if_not_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in'):
            flash('You are already logged in.')
            return redirect(url_for('show_messages'))
        return f(*args, **kwargs)
    return decorated_function
