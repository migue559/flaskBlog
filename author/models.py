


class Author():
	id=0
	fullname=''
	email=''
	username=''
	password=''
	is_author=True

	def __init__(self,fullname,email,username,password,is_author=False):
		self.fullname=fullname
		self.email=email
		self.username=username
		self.password=password
		self.is_author=is_author

	def __repr__(self):
		return "<Author %r>" % self.username
