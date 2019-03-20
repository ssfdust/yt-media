from flask import Flask
from ext import db, login_manager, ckeditor, rest_api
from admin import admin
#  from flask_cors import CORS

app = Flask(__name__, static_folder='uploads')
app.config['CKEDITOR_FILE_UPLOADER'] = 'ck_upload'
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/yt_media'
app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.config['OPENAPI_REDOC_PATH'] = 'redoc'
app.config['OPENAPI_REDOC_VERSION'] = 'next'
app.config['OPENAPI_SWAGGER_UI_PATH'] = 'swagger'
app.config['OPENAPI_SWAGGER_UI_VERSION'] = '3.21.0'
app.config['OPENAPI_URL_PREFIX'] = 'doc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8\r{A#!|Dz\n\xec]/'

db.init_app(app)
admin.init_app(app)
login_manager.init_app(app)
ckeditor.init_app(app)
rest_api.init_app(app)

from views import * # NOQA
rest_api.register_blueprint(blp) # NOQA


if __name__ == '__main__':

    app.run(host='0.0.0.0',
            debug=True)
