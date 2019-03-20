import os

from flask import (
    jsonify, render_template, request, send_from_directory, url_for
)
from flask.views import MethodView
from flask_ckeditor import upload_fail, upload_success
from flask_login import current_user, login_required, login_user, logout_user
from flask_rest_api import Blueprint

from app import app, db
from models import Comment, Person, Story, Tag, Topic, User
from schema import (
    BaseArgSchema, CommentSchema, InfoRetSchema, LoginMsgSchema, LoginSchema,
    MsgSchema, PersonRetSchema, StoryArgSchema, StoryItemSchema, CmtRetSchema,
    StoryRetSchema, StorySchema, TagArgSchema, TagRetSchema, TopicRetSchema
)
from utils import gen_hash_filename, generate_md5

file_path = os.path.join(os.path.dirname(__file__), 'uploads')
blp = Blueprint(
    'Api', 'api', url_prefix='/api',
    description='yt-media REST api'
)

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

@blp.route('/login')
class Login(MethodView):
    @blp.doc(summary='用户登录',
             description='用户登录')
    @blp.arguments(LoginSchema)
    @blp.response(LoginMsgSchema, code=200)
    def post(self, login_info):
        user = User.query.filter_by(username=login_info['username']).first()
        if user and user.check_password(login_info['password']):
            login_user(user)
            return jsonify({'code': 0, 'username': user.username, 'msg': 'success'})
        elif user:
            return jsonify({'code': 403, 'msg': 'wrong password'})
        else:
            return jsonify({'code': 404, 'msg': 'user doesn\'t exsit'})

@blp.route('/userinfo')
class UserInfo(MethodView):
    @login_required
    @blp.doc(summary='获取用户信息',
             description='获取用户信息')
    @blp.response(InfoRetSchema, code=200)
    def get(self):
        return jsonify({'code': 0, 'userinfo': {'username': current_user.username,
                                                'flag': current_user.flag}})

@blp.route('/register')
class Register(MethodView):
    @blp.arguments(LoginSchema)
    @blp.doc(summary='注册用户', description='注册用户')
    @blp.response(MsgSchema, code=200)
    def post(self, login_info):
        user = User.query.filter_by(username=login_info['username']).first()
        if user:
            return {'code': 403, 'msg': 'user already exsits'}
        else:
            user = User(username=login_info['username'],
                        password=generate_md5(login_info['password']))
            db.session.add(user)
            db.session.commit()
            return {'code': 0, 'msg': 'create successfully'}

@blp.route('/logout')
class Logout(MethodView):
    @login_required
    @blp.doc(summary='用户登出', description='用户登出')
    @blp.response(MsgSchema, code=200)
    def get(self):
        logout_user()
        return {'code': 0, 'msg': 'success'}

@app.route('/index')
def index():
    return render_template('index.html')

@blp.route('/persons')
class PersonView(MethodView):
    @blp.doc(summary='获取人物详情', description='获取人物详情')
    @blp.arguments(BaseArgSchema, location='query')
    @blp.response(PersonRetSchema)
    def get(self, args):
        num = args.get('number')
        person_id = args.get('id')
        persons = Person.query
        if person_id:
            persons = persons.filter_by(id=person_id)
        items = persons.order_by(Person.create_time.desc()).limit(num).all()
        return {
            'data': items,
            'total': len(items),
            'code': 0
        }

@blp.route('/topics', methods=['GET'])
class TopicView(MethodView):
    @blp.doc(summary='获取主题详情', description='获取主题详情')
    @blp.arguments(BaseArgSchema, location='query')
    @blp.response(TopicRetSchema)
    def get(self, args):
        num = args.get('num')
        topic_id = args.get('id')

        topics = Topic.query
        if topic_id:
            topics = topics.filter_by(id=topic_id)
        items = topics.order_by(Topic.create_time.desc()).limit(num).all()

        return {
            'data': items,
            'total': len(items),
            'code': 0
        }

@blp.route('/tags', methods=['GET'])
class TagView(MethodView):
    @blp.doc(summary='获取标签（精选）详情',
             description='is_great参数用以获取是否为精选内容'
                            '带上tag的id也是只会搜索精选中的id')
    @blp.arguments(TagArgSchema, location='query')
    @blp.response(TagRetSchema)
    def get(self, tag_args):
        num = tag_args.get('number')
        tag_id = tag_args.get('id')
        is_great = tag_args.get('is_great')
        print(is_great)
        tags = Tag.query
        if tag_id:
            tags = tags.filter_by(id=tag_id)

        if is_great:
            tags = tags.filter_by(is_great=is_great)

        items = tags.order_by(Tag.create_time.desc()).limit(num).all()

        return {
            'data': items,
            'total': len(items),
            'code': 0
        }

@blp.route('/story', methods=['GET'])
class GetStory(MethodView):
    @blp.doc(summary='搜索故事详情',
             description='所有故事搜索都可以用这个接口<br>'
                            'name字段可以用于搜索框<br>'
                            '热门内容为')
    @blp.arguments(StoryArgSchema, location='query')
    @blp.response(StoryRetSchema)
    def get(self, story_args):
        person_id = story_args.get('person_id')
        tag_id = story_args.get('tag_id')
        topic_id = story_args.get('topic_id')
        hot = story_args.get('hot')
        name = story_args.get('name')
        number = story_args.get('num')

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
            items = stories.order_by(Story.create_time.desc()).limit(number).all()
        else:
            items = stories.order_by(Story.hits.desc()).limit(number).all()

        return {
            'code': 0,
            'total': len(items),
            'data': items
        }

@blp.route('/story/item', methods=['GET'])
class StoryItemView(MethodView):
    @blp.doc(summary='单个故事详情',
             description='根据ID返回整个故事内容')
    @blp.arguments(BaseArgSchema(only=('id',)), location='query')
    @blp.response(StoryItemSchema)
    @blp.response(MsgSchema)
    def get(self, args):
        story_id = args.get('id')

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

@blp.route('/comment')
class CommentView(MethodView):
    @blp.doc(summary='单个故事评论',
             description='根据故事ID返回整个故事评论')
    @blp.arguments(BaseArgSchema(only=('id',)), location='query')
    @blp.response(CmtRetSchema())
    def get(self, args):
        print(args)
        story_id = args.get('id')
        comments = Comment.query.filter_by(story_id=story_id).all()

        return {
            'code': 0,
            'total': len(comments),
            'data': comments
        }

    @login_required
    @blp.doc(summary='评论单个故事',
             description='根据故事ID提交评论')
    @blp.arguments(CommentSchema(only=['comment', 'id']))
    @blp.response(MsgSchema)
    def post(self, args):
        json = request.get_json(force=True)
        comment = Comment(uid=current_user.id, **json)
        db.session.add(comment)
        db.session.commit()

        return {
            'code': 0,
            'msg': 'create successfully'
        }
