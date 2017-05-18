from flask import Flask
from flask_mongoalchemy import MongoAlchemy
#from markdown2 import Markdown

app =Flask(__name__)
app.config.from_object('settings')
db = MongoAlchemy(app)


#markdown
#markdown=Markdown(app)

from blog import views
from author import views
