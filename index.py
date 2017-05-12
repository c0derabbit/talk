from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
	return 'Hello World!'

@app.route('/yo')
def yo():
	return 'foobar'

@app.route('/msg/<string:name>')
def message_user(name):
	return 'user %s' % name

@app.route('/test')
def test():
	return url_for('message_user', name='Sam')

if __name__ == '__main__':
	app.run()
