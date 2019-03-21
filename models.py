from ext import db, login_manager
from sqlalchemy.dialects.mysql import TIMESTAMP, LONGTEXT
from sqlalchemy import func
from utils import generate_md5

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, doc='用户表主键')
    username = db.Column(db.String(100), nullable=False, unique=True, doc='用户名')
    password = db.Column(db.String(100), nullable=False, doc='用户密码')
    flag = db.Column(db.Integer, nullable=False, default=1, doc='用户标记 1为普通用户 2为管理员 默认为1')
    create_time = db.Column(TIMESTAMP, default=func.now(), doc='创建时间')

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        if self.password == generate_md5(password):
            return True
        else:
            return False

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return "{}".format(self.username)

class Topic(db.Model):

    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True, doc='主题主键')
    name = db.Column(db.String(100), nullable=False, doc='主题名称')
    thumbnail = db.Column(db.String(512), nullable=False, doc='封面图片')
    description = db.Column(db.String(1000), nullable=False, doc='主题描述')
    create_time = db.Column(TIMESTAMP, default=func.now(), doc='创建时间')
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    user = db.relationship(User)

    def __repr__(self):
        return "{}".format(self.name)

class Person(db.Model):

    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True, doc='人物ID')
    name = db.Column(db.String(100), nullable=False, doc='人物名称')
    thumbnail = db.Column(db.String(512), nullable=False, doc='人物封面')
    description = db.Column(db.String(1000), nullable=False, doc='人物描述')
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1,
                    doc='创建人ID默认为管理员')
    create_time = db.Column(TIMESTAMP, default=func.now(), doc='创建时间')
    user = db.relationship(User, doc='创建人')

    def __repr__(self):
        return "{}".format(self.name)

class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, doc='标签主键')
    name = db.Column(db.String(100), nullable=False, doc='标签名称')
    description = db.Column(db.String(1000), nullable=False, doc='标签描述')
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    is_great = db.Column(db.Boolean, nullable=False, default=False, doc='是否为精品')
    create_time = db.Column(TIMESTAMP, default=func.now())
    user = db.relationship(User)

    def __repr__(self):
        return "{}".format(self.name)

class Story(db.Model):

    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True, doc='故事主键')
    name = db.Column(db.String(100), nullable=False, doc='故事名称')
    description = db.Column(db.String(1000), nullable=False, doc='故事描述')
    text = db.Column(LONGTEXT, doc='故事文本')
    thumbnail = db.Column(db.String(512), nullable=False, doc='故事缩略图')
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1,
                    doc='创建人ID 默认为1管理员')
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    hits = db.Column(db.Integer, default=0)
    create_time = db.Column(TIMESTAMP, default=func.now())
    user = db.relationship(User, doc='创建用户')
    tag = db.relationship(Tag, doc='关联的标签')
    person = db.relationship(Person, doc='关联的人物')
    topic = db.relationship(Topic, doc='关联的主题')

    def __repr__(self):
        return "{}".format(self.name)

class Comment(db.Model):

    __tablename__ = 'story_comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(512), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    create_time = db.Column(TIMESTAMP, default=func.now())
    user = db.relationship(User)

    story = db.relationship(Story, backref='comments', uselist=False)

    def __repr__(self):
        return "{}".format(self.comment)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()
