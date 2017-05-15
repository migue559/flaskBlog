from flask_wtf import Form
from wtforms  import validators , StringField,TextAreaField,SelectField
from author.form import RegisterForm
from blog.models import Category
from mongo import mongo_objects

class SetupForm(RegisterForm):
	name=StringField('Blog name', [
		validators.Required(),
		validators.Length(max=80)
		])

def categories():
	return Category

class PostForm(Form):
	title=StringField('title',[
		validators.Required(),
		validators.Length(max=80)
		])
	body= TextAreaField('Content',[validators.Required()])
	category= SelectField(u'Category')
	new_category = StringField('New Category')	
