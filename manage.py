import os, sys
file_item_path= os.path.join(os.path.dirname(__file__),"flaskBlog\Lib\site-packages") 
sys.path.append(file_item_path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))             

from flask_script import Manager, Server
from flaskBlog import app,db


manager= Manager(app)


manager.add_command('runserver', Server(
	use_debugger=True,
	use_reloader=True,
	host=os.getenv('IP','127.0.0.1'),
	port= int(os.getenv('PORT',5000))
	)
)

if __name__== '__main__':
	manager.run()

