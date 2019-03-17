from flask import jsonify, request, url_for, send_from_directory, render_template
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from schema import PersonSchema, StorySchema, TagSchema, TopicSchema, CommentSchema
from models import User, Topic, Person, Tag, Story, Comment
from utils import generate_md5, gen_hash_filename
from flask_ckeditor import upload_success, upload_fail

import os

file_path = os.path.join(os.path.dirname(__file__), 'uploads')

@app.route('/ckfiles/<path:filename>')
def ck_uploaded_files(filename):
    return send_from_directory(file_path, filename)

@app.route('/upload', methods=['POST'])
def ck_upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    filename = gen_hash_filename(None, f)
    f.save(os.path.join(file_path, filename))
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
@login_required
def logout():
    logout_user()
    return jsonify({'code': 0, 'msg': 'success'})

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/api/persons', methods=['POST', 'GET'])
def fetch_persons():
    num = request.args.get('number', 1, type=int)
    person_id = request.args.get('id', None, type=int)
    persons = Person.query
    if person_id:
        persons = persons.filter_by(id=person_id)
    items = persons.order_by(Person.create_time.desc()).limit(num).all()
    schema = PersonSchema(many=True)
    ret = schema.dump(items)
    return jsonify({
        'data': ret,
        'total': num,
        'code': 0
    })

@app.route('/api/topics', methods=['GET'])
def fet_topics():
    num = request.args.get('num', 1, type=int)
    topic_id = request.args.get('id', None, type=int)

    topics = Topic.query
    if topic_id:
        topics = topics.filter_by(id=topic_id)
    items = topics.order_by(Topic.create_time.desc()).limit(num).all()
    schema = TopicSchema(many=True)

    ret = schema.dump(items)

    return jsonify({
        'data': ret,
        'total': len(items),
        'code': 0
    })

@app.route('/api/tags', methods=['GET'])
def fetch_tags():
    num = request.args.get('number', 1, type=int)
    tag_id = request.args.get('id', None, type=int)
    is_great = request.args.get('is_great', False, type=int)
    tags = Tag.query
    if tag_id:
        tags = tags.filter_by(id=tag_id)

    if is_great:
        tags = tags.filter_by(is_great=is_great)

    items = tags.order_by(Tag.create_time.desc()).limit(num).all()
    schema = TagSchema(many=True)

    ret = schema.dump(items)

    return jsonify({
        'data': ret,
        'total': len(items),
        'code': 0
    })

@app.route('/api/story', methods=['GET'])
def fetch_story():
    person_id = request.args.get('person_id', None, type=int)
    tag_id = request.args.get('tag_id', None, type=int)
    topic_id = request.args.get('topic_id', None, type=int)
    hot = request.args.get('hot', False, type=bool)
    name = request.args.get('name', None)

    # 去除指定的栏目以减小数据大小
    exclude_cols = [i for i in request.args.get('exclude', ',').split(',') if i != '']

    stories = Story.query
    if person_id:
        stories = stories.filter_by(person_id=person_id)

    if tag_id:
        stories = stories.filter_by(tag_id=tag_id)

    if topic_id:
        stories = stories.filter_by(topic_id=topic_id)

    if name:
        stories = stories.filter(Story.name.like('%{}%'.format(name)))

    if hot:
        items = stories.order_by(Story.create_time.desc()).all()
    else:
        items = stories.order_by(Story.hits.desc()).all()

    schema = StorySchema(many=True, exclude=exclude_cols)

    ret = schema.dump(items)

    return jsonify({
        'code': 0,
        'data': ret,
    })

@app.route('/api/story/item', methods=['GET'])
def fetch_story_item():
    story_id = request.args.get('id')

    story = Story.query.filter_by(id=story_id).first()

    if story:
        schema = StorySchema()
        ret = schema.dump(story)

        # 统计点击量
        story.hits = story.hits + 1
        db.session.add(story)
        db.session.commit()

        return jsonify({
            'code': 0, 
            'data': ret
        })
    else:
        return jsonify({
            'code': 1,
            'msg': 'story doesn\'t exist'
        })

@app.route('/api/comment', methods=['GET', 'POST'])
@login_required
def create_or_get_post():
    if request.method == 'GET':
        story_id = request.args.get('id')
        comments = Comment.query.filter_by(story_id=story_id).all()
        schema = CommentSchema(many=True)

        ret = schema.dump(comments)

        return jsonify({
            'code': 0,
            'data': ret
        })
    elif request.method == 'POST':
        json = request.get_json(force=True)
        comment = Comment(uid=current_user.id, **json)
        db.session.add(comment)
        db.session.commit()

        return jsonify({
            'code': 0,
            'msg': 'create successfully'
        })
