import os

dev_env = dict(
	# DATABASE=os.path.join(app.root_path, 'talk.db'),
	DATABASE_URL='/tmp/talk.db',
	SECRET_KEY='dev key',
)

prod_env = dict(
	DATABASE_URL='postgres://vvyvnusnxnfagn:f7093437d20db7220f34a36937223cef47cb313a25d3815a6ba544193bbd21f9@ec2-54-75-231-195.eu-west-1.compute.amazonaws.com:5432/dd6ub0ojujlq6q',
	SECRET_KEY='blahwillsetthislater'
)
