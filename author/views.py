from flaskBlog import app
from flask import  render_template, redirect, url_for ,flash,session,request
from author.form import RegisterForm, LoginForm
from author.models import Author
from mongo import mongo_objects
from author.decorators import login_required
import bcrypt


@app.route('/login', methods=('GET','POST'))
def login():
	form=LoginForm()
	error=None
	if request.method == 'GET' and request.args.get('next'):
		session['next'] = request.args.get('next', None)

	if form.validate_on_submit():
		usr=form.username.data
		#pwd=form.password.data
		author=mongo_objects.find_login_operation(usr)
		if author:
			mongo_usr=author[0]
			mongo_pwd=author[1]
			mongo_author=author[2]
			if usr == mongo_usr and bcrypt.hashpw((form.password.data).encode('utf-8'), mongo_pwd.encode('utf-8')) == mongo_pwd.encode('utf-8'):
				session['username'] = usr
				session['is_author'] = mongo_author
				if 'next' in session:
					next= session.get('next')
					session.pop('next')
					return redirect(next)
				else:
					return redirect('/login_suceess')
			else:
				error="Incorrect password"
		else:
			error="author invalid try again!"
			#return redirect(url_for('login_wrong'))
	return render_template('author/login.html',form=form, error=error)


@app.route('/register', methods=('GET','POST'))
def register():
	form= RegisterForm()
	if form.validate_on_submit():
		return redirect(url_for('successs'))
	return render_template('author/register.html',form=form)

@app.route('/successs')
def successs():
	return "Registration successs"


@app.route('/login_suceess')
@login_required
def login_suceess():
	return "Login login_suceess"

@app.route('/login_wrong')
def login_wrong():
	flash('user o password invalid try again!')     
	return redirect('/login')

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect(url_for('index'))

