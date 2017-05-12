import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),"flaskBlog\Lib\site-packages")) 
print(os.path.dirname(__file__))

from flask import Flask
#from markdown2 import Markdown



app =Flask(__name__)


app.config.from_object('settings')


#markdown
#markdown=Markdown(app)

from blog import views
from author import views


