import datetime

class Blog():
	id  = 0
	name="miguel"
	admin=1
	#posts =db.relationship('Post', backref='blog',lazy='dynamic')

	def __init__(self, name, admin):
		self.name = name
		self.admin = admin

	def __repr__(self):
		return "<Name %r>" % self.name

class Post():
	id=0
	blod_id=0
	author_id=0
	title=""
	body=""
	slug=""
	publish_date=datetime.datetime.now()
	live=True
	category_id=0

	def __init__(self, blog,author,title,body,category,slug=None,publish_date=None,live=True):
		self.blod_id=blog
		self.author_id=author
		self.title=title
		self.body=body
		self.slug=slug
		if self.publish_date is None:
			self.publish_date=datetime.datetime.utcnow()
		else:
			self.publish_date=publish_date
		self.live=live
		self.category_id=category

	def __repr__(self):
		return "<Post %r>" % self.title

class Category():
	id=0
	name=[]

	def __init__(self,name):
		self.name=name

	def __repr__(self):
		return "<Category %r>" %self.name





