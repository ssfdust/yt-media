from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor

db = SQLAlchemy()
admin = Admin()
login_manager = LoginManager()
ckeditor = CKEditor()
