from flask import Flask
from ext import db, login_manager, ckeditor
from admin import admin
#  from flask_cors import CORS

app = Flask(__name__, static_folder='uploads')
app.config['CKEDITOR_FILE_UPLOADER'] = 'ck_upload'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:24WKisxian@localhost/yt_media'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.secret_key = b'_5#y2L"F4Q8\r{A#!|Dz\n\xec]/'

db.init_app(app)
admin.init_app(app)
login_manager.init_app(app)
ckeditor.init_app(app)


from views import *

if __name__ == '__main__':

    app.run(host='0.0.0.0',
            debug=True)
