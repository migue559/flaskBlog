from flask_wtf import Form
from wtforms  import validators , StringField,TextAreaField,SelectField
from author.form import RegisterForm
from blog.models import category, Post
from mongo import mongo_objects

class SetupForm(RegisterForm):
	name=StringField('Blog name', [
		validators.Required(),
		validators.Length(max=80)
		])

def categories():
	return Category

class PostForm(Form):
	document_class = Post
	title=StringField('title',[	validators.Required(),		validators.Length(max=80)		])
	body= TextAreaField('Content',[validators.Required()])
	category= SelectField(u'Category')
	new_category = StringField('New Category')	
	instance = None

	def __init__(self, document=None, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		if document is not None:
			self.instance = document
			self._copy_data_to_form()

	def _copy_data_to_form(self):
		self.title.data = self.instance.title
		self.body.data = self.instance.body
		#self.category.data = self.instance.category
		#self.new_category.data = self.instance.new_category

	def save(self):
		if self.instance is None:
			self.instance = self.document_class()
		self.instance.title = self.title.data
		self.instance.body = self.body.data
		self.instance.category = self.category.data
		self.instance.new_category = self.new_category.data
		self.instance.save()
		return self.instance

