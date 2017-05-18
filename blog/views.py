from flaskBlog import app
from mongo import mongo_objects
from flask import render_template, redirect, url_for, flash, session
from blog.form import SetupForm   , PostForm, category
from author.models import Author
from blog.models import Blog, Post, Author, category
from author.decorators import login_required, author_required
import bcrypt
import datetime


@app.route('/')
@app.route('/index/<int:page>')
def index(page=1):
	usr=session['username']
	posts=Post.query.paginate(page=page, per_page=5)
	author_id=Author.query.filter(Author.username==usr).first()
	blog=Blog.query.filter(Blog.id ==  author_id.id ).first()
	categ=category.query.filter(category.id ==  1).first()
	return render_template('blog/index.html',posts=posts, blog=blog, author=author_id, category=categ)


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


@app.route('/saveBlogAuthor/<fullname>/<email>/<username>/<password>/<blog>')
def saveBlogAuthor(fullname,email,username,password,blog):
	A=mongo_objects.id_blog_author()
	id_author=A[0]
	id_blog=A[1]
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
	except:
		return "no se hizo la creacion del blog"

@app.route('/article/<title>/<body>/<category>')
@login_required
def article(title:None,body=None,category=None):
	_post=Post(blog_id=1, author_id=1, title=title, body=body, category_id=2)
	return render_template('blog/article.html',post=_post)		

@app.route('/post', methods=('GET','POST'))
@author_required
def post():
	form=PostForm()
	form.category.choices = [   ( str(item["id"]),item["name"] ) for item in mongo_objects.find_categories() ]
	if  form.validate_on_submit():
		if form.new_category.data:
			new_category = form.new_category.data
			_category = new_category
		else:
			new_category='no'
			_category = form.category.data
		return redirect(url_for('savePost',
			title=form.title.data,
			body=form.body.data,
			category=_category,
			new_category=new_category))
	return render_template('/blog/post.html', form=form)


@app.route('/savePost/<title>/<body>/<category>/<new_category>/')
def savePost(title=None,body=None,category=None,new_category=None):	
	usr=session['username']
	_title=title
	_body=body
	_category=category
	_new_category=new_category
	if new_category=='no':
		#if  valida que los datos no esten repetidos
		mongo_objects.insert_post(title,body,usr,category)
		flash('post with created')
		return redirect(url_for('article',title=_title,body=_body,category=_category))

	else:
		#if  valida que los datos no esten repetidos
		mongo_objects.insert_category(new_category)
		mongo_objects.insert_post(title,body,usr,category)
		flash('post with new category created')
		return redirect(url_for('article',title=_title,body=_body,category=_new_category))


