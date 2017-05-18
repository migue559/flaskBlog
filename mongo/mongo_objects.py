from flaskBlog import app
from flask_pymongo import PyMongo
from blog.models import Blog, Post
import datetime

app.config['MONGO_DBNAME']='flaskPython'
app.config['MONGO_URI']='mongodb://127.0.0.1:27017/flaskPython'


mongo = PyMongo(app)	#contiene la conexion a mongo

def count_blog():
	cnt=0
	blog=mongo.db.Blog
	num_reg=blog.find().count()
	if num_reg==None:
		return cnt
	else:
		return num_reg


def get_max_id(_collection):
	id=[]
	if _collection=='blog':
		collection=mongo.db.Blog
	if _collection=='post':
		collection=mongo.db.Post
	if _collection=='author':
		collection=mongo.db.Author
	max_id=collection.find().sort([('id', -1)]).limit(1)   #recupera el ultimo id de la colleccion author
	for reg in max_id:
		id.append(reg['id'])
	return id



def get_id_author():
	id=[]
	author=mongo.db.Author
	max_id=author.find().sort([('id', -1)]).limit(1)   #recupera el ultimo id de la colleccion author
	for reg in max_id:
		id.append(reg['id'])
	return id

def get_id_blog():
	id=[]
	blog=mongo.db.Blog
	max_id=blog.find().sort([('id', -1)]).limit(1)   #recupera el ultimo id
	for reg in max_id:
		id.append(reg['id'])
	return id


def find_login_operation(usr):
	b=[]
	collection=mongo.db.Author
	a =collection.find({'username':usr})
	for reg in a:
		b.append(reg['username'])
		b.append(reg['password'])
		b.append(reg['is_author'])
	return b

def find_categories():
	category=mongo.db.category
	a =category.find()
	return a

def update_operation():
	return True

def remove_operation():
	return True	


def insert_blog_operation(id,blog,admin):
	coll_blog=mongo.db.Blog
	coll_blog.insert({'id': id ,'blog': blog, 'admin':admin })
	return True


def insert_author_operation(id, fullname,email,username,password,is_author=False):
	coll_author=mongo.db.Author
	coll_author.insert({'id': id,'fullname':fullname,'email':email,'username': username,'password':password,'is_author':is_author})
	return True

def insert_category(new_category):
	id=[]
	coll_category=mongo.db.category
	max_id=coll_category.find().sort([('id', -1)]).limit(1)   #recupera el ultimo id de la colleccion author
	for reg in max_id:
		id.append(reg['id'])
	id_=id[0]+1
	coll_category.insert({'id':id_,'name':new_category})
	return True

def insert_post(title,body,usr,category):
	_id_post=0
	coll_post=mongo.db.Post
	coll_blog=mongo.db.Blog
	coll_author=mongo.db.Author
	author_id=[]
	blog_id=[]
	id_a=coll_author.find({'username':usr},{'id':1,'_id':0})
	for reg in id_a:
		author_id.append(reg['id'])
	id_b=coll_blog.find({'admin':author_id[0]},{'admin':1,'id':1,'_id':0})
	for reg in id_b:
		blog_id.append(reg['id'])
	post_id=get_max_id('post')
	if post_id:
		_id_post=post_id[0]
	else:
		_id_post=0
	if _id_post==None:
		_id_post=1
	else:
		_id_post+=1
	slug=None
	publish_date=datetime.datetime.now()
	live=True
	category_id=category
	coll_post.insert({'id':_id_post,
					  'blog_id':blog_id[0],
					  'author_id':author_id[0],
					  'title':title,
					  'body':body,
					  'slug':slug,
					  'publish_date':publish_date,
					  'live':live,
					  'category_id':category})
	return True



def id_blog_author():
	A=[]
	max_id_author=get_max_id('author')
	max_id_blog=get_max_id('blog')
	if max_id_author and max_id_blog:
		id_author=max_id_author[0]
		id_blog=max_id_blog[0]
	else:
		id_author=0
		id_blog=0
	if id_author==None or id_blog==None:
		id_author=1
		id_blog=1
	else:
		id_author+=1
		id_blog+=1
	A=[id_author,id_blog]
	return A

def get_posts():
	posts=[]
	collection=mongo.db.Post
	a =collection.find({"id": {"$lt": 10}}).sort([("id", 1), ("publish_date", -1)])
	return a

