from flaskBlog import app
from mongo import mongo_objects
from flask import render_template, redirect, url_for, flash
from blog.form import SetupForm   , PostForm
from author.models import Author
from blog.models import Blog
from mongo import mongo_objects
from author.decorators import login_required, author_required
import bcrypt


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
		blog = Blog(form.name.data,1)#author.id)
		
		return redirect(url_for('test',
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
	form.category.choices = [   ( item["id"],item["name"] ) for item in mongo_objects.find_categories()  ]
	return render_template('/blog/post.html', form=form)

@app.route('/article')
@login_required
def article():
	return render_template('blog/article.html')


@app.route('/test/<fullname>/<email>/<username>/<password>/<blog>')
def test(fullname,email,username,password,blog):
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



