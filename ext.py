from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_rest_api import Api

db = SQLAlchemy()
admin = Admin(base_template='my_master.html')
login_manager = LoginManager()
ckeditor = CKEditor()
rest_api = Api()
