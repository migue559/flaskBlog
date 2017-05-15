from flaskBlog import app
from mongo import mongo_objects
from flask import render_template, redirect, url_for, flash, session
from blog.form import SetupForm   , PostForm, Category
from author.models import Author
from blog.models import Blog, Post
from mongo import mongo_objects
from author.decorators import login_required, author_required
import bcrypt
import datetime


@app.route('/')
@app.route('/index')
def index():	
	return "Kola hola" 

@app.route('/admin')
@author_required
def admin():
	blogs=mongo_objects.count_blog()
	if blogs == 0:
		return redirect(url_for('setup'))
	return render_template('blog/admin.html')

@app.route('/setup', methods=('GET','POST'))
def setup():
	form=SetupForm()
	if form.validate_on_submit():
		salt=bcrypt.gensalt()
		hashed_password=bcrypt.hashpw((form.password.data).encode('utf-8'), salt)
		author= Author(
			form.fullname.data,
			form.email.data,
			form.username.data,
			hashed_password,
			True)
		blog = Blog(form.name.data,1)
		return redirect(url_for('saveBlogAuthor',
			fullname=author.fullname,
			email=author.email,
			username=author.username,
			password=hashed_password,
			blog=blog.name
			))
	return render_template('blog/setup.html', form=form)

@app.route('/post', methods=('GET','POST'))
@author_required
def post():
	form=PostForm()
	form.category.choices = [   ( str(item["id"]),item["name"] ) for item in mongo_objects.find_categories() ]
	if  form.validate_on_submit():
		if form.new_category.data:
			new_category = form.new_category.data
			category = new_category
		else:
			new_category='no'
			category = form.category.data
		Blog=username=session['username']
		title=form.title.data
		body=form.body.data
		slug=None
		post=""
		return redirect(url_for('savePost',title=title,body=body,category=category,new_category=new_category,Blog=Blog))
	return render_template('/blog/post.html', form=form)

@app.route('/article')
@login_required
def article():
	return render_template('blog/article.html')


@app.route('/saveBlogAuthor/<fullname>/<email>/<username>/<password>/<blog>')
def saveBlogAuthor(fullname,email,username,password,blog):
	max_id_author=mongo_objects.get_id_author()
	max_id_blog=mongo_objects.get_id_blog()
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
	fullname=fullname
	email=email
	username=username
	password=password
	blog=blog
	try:
		mongo_objects.insert_author_operation(id_author,fullname,email,username,password,is_author=True)
		mongo_objects.insert_blog_operation(id_blog,blog,id_author)
		flash('Blog created')
		return redirect('/admin')
		#return "fullname: %s email: %a username: %s password: %s blog: %s max id_author: %s id_blog: %s" % (fullname,email,username,password,blog,id_author,id_blog)
	except:
		return "no se hizo la creacion del blog"

@app.route('/savePost/<title>/<body>/<category>/<new_category>/<Blog>')#/<body>/<category>/<new_category>', methods=('GET','POST'))
def savePost(title=None,body=None,category=None,new_category=None,Blog=None):	
	if new_category=='no':
		return "AAAAA   TITLE: %s BODY: %s  CATEGORY: %s NEW CAT: %s  y blog %s" % (title, body, category, new_category, Blog)
		
	else:
		mongo_objects.insert_category(new_category)
		return "TITLE: %s BODY: %s  CATEGORY: %s NEW CAT: %s y body %s" % (title, body, category, new_category,Blog)#redirect('/admin')
	#try:
		#mongo_objects.insert_author_operation(id_author,fullname,email,username,password,is_author=True)
		#mongo_objects.insert_blog_operation(id_blog,blog,id_author)
		#flash('Post created')
		#return "fullname: %s email: %a username: %s password: %s blog: %s max id_author: %s id_blog: %s" % (fullname,email,username,password,blog,id_author,id_blog)
	#except:
	#	return "no se hizo la creacion del Post"		







