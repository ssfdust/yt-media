from flask import jsonify, request, url_for, send_from_directory, render_template
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from models import User, Topic, Person, Tag, Story
from utils import generate_md5, gen_hash_filename
from flask_ckeditor import upload_success, upload_fail

import os

file_path = os.path.join(os.path.dirname(__file__), 'uploads')
ck_path = os.path.join(os.path.dirname(__file__), 'ckfiles')

@app.route('/ckfiles/<path:filename>')
def ck_uploaded_files(filename):
    return send_from_directory(ck_path, filename)

@app.route('/upload', methods=['POST'])
def ck_upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    filename = gen_hash_filename(None, f)
    f.save(os.path.join(ck_path, filename))
    url = url_for('ck_uploaded_files', filename=filename)
    return upload_success(url=url)

@app.route('/api/login', methods=['POST'])
def login():
    json = request.get_json(force=True)
    user = User.query.filter_by(username=json['username']).first()
    if user and user.check_password(json['password']):
        login_user(user)
        return jsonify({'code': 0, 'username': user.username, 'msg': 'success'})
    elif user:
        return jsonify({'code': 403, 'msg': 'wrong password'})
    else:
        return jsonify({'code': 404, 'msg': 'user doesn\'t exsit'})

@app.route('/api/userinfo', methods=['GET'])
@login_required
def userinfo():
    return jsonify({'code': 0, 'userinfo': {'username': current_user.username,
                                            'flag': current_user.flag}})

@app.route('/api/register', methods=['POST'])
def register():
    json = request.get_json(force=True)
    user = User.query.filter_by(username=json['username']).first()
    if user:
        return jsonify({'code': 403, 'msg': 'user already exsits'})
    else:
        user = User(username=json['username'],
                    password=generate_md5(json['password']))
        db.session.add(user)
        db.session.commit()
        return jsonify({'code': 0, 'msg': 'create successfully'})

@app.route('/api/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return jsonify({'code': 0, 'msg': 'success'})

@app.route('/index')
def index():
    return render_template('index.html')
