from flaskBlog import app
from flask_pymongo import PyMongo

app.config['MONGO_DBNAME']='flaskPython'
app.config['MONGO_URI']='mongodb://127.0.0.1:27017/flaskPython'
mongo = PyMongo(app)	#contiene la conexion a mongo

def count_blog():
	cnt=0
	blog=mongo.db.blog
	num_reg=blog.find().count()
	if num_reg==None:
		return cnt
	else:
		return num_reg

def get_id_author():
	id=[]
	author=mongo.db.author
	max_id=author.find().sort([('id', -1)]).limit(1)   #recupera el ultimo id de la colleccion author
	for reg in max_id:
		id.append(reg['id'])
	return id

def get_id_blog():
	id=[]
	blog=mongo.db.blog
	max_id=blog.find().sort([('id', -1)]).limit(1)   #recupera el ultimo id
	for reg in max_id:
		id.append(reg['id'])
	return id


def find_login_operation(usr):
	b=[]
	collection=mongo.db.author
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
	coll_blog=mongo.db.blog
	coll_blog.insert({'id': id ,'blog': blog, 'admin':admin })
	return True


def insert_author_operation(id, fullname,email,username,password,is_author=False):
	coll_author=mongo.db.author
	coll_author.insert({'id': id,'fullname':fullname,'email':email,'username': username,'password':password,'is_author':is_author})
	return True


