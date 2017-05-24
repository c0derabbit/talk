import os

dev_env = dict(
	# DATABASE=os.path.join(app.root_path, 'talk.db'),
	DATABASE='/tmp/talk.db',
	SECRET_KEY='dev key',
	USER1='eszter',
	USER2='Samu',
	PASSWORD='secret'
)

prod_env = dict(
)
