import os

prod_env = dict(
	DATABASE_URL=os.environ.get('DATABASE_URL'),
	SECRET_KEY=os.environ.get('SECRET_KEY')
)
