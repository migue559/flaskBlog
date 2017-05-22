from flaskBlog import app
from flaskBlog import db
from mongo import mongo_objects
from flask_mongoalchemy import BaseQuery
import datetime


class Author(db.Document):
	id = db.IntField()
	fullname = db.StringField()
	email = db.StringField()
	username = db.StringField()
	password = db.StringField()
	is_author = db.BoolField()

class PostQuery(BaseQuery):

	def filter_by_active(self):
		return self.filter({'live': True})

	def editPost(self):
		#id=float(id_post)
		return self.filter({'id':2})

class Post(db.Document):
	query_class = PostQuery
	id=db.FloatField()
	blog_id=db.FloatField()
	author_id=db.FloatField()
	title=db.StringField()
	body=db.StringField()
	Slug=db.FloatField()
	publish_date=db.DateTimeField()
	live=db.BoolField()
	category_id=db.FloatField()


class Blog(db.Document):
	id  =db.FloatField()
	blog=db.StringField()
	admin=db.FloatField()


class category(db.Document):
	id=db.FloatField()
	name=db.StringField()


