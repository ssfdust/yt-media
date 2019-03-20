from ext import db, login_manager
from sqlalchemy.dialects.mysql import TIMESTAMP, LONGTEXT
from sqlalchemy import func
from utils import generate_md5

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    flag = db.Column(db.Integer, nullable=False, default=1)
    create_time = db.Column(TIMESTAMP, default=func.now())

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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    create_time = db.Column(TIMESTAMP, default=func.now())
    user = db.relationship(User)

    def __repr__(self):
        return "{}".format(self.name)

class Person(db.Model):

    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True, comment='人物ID')
    name = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    create_time = db.Column(TIMESTAMP, default=func.now())
    user = db.relationship(User)

    def __repr__(self):
        return "{}".format(self.name)

class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    is_great = db.Column(db.Boolean, nullable=False, default=False)
    create_time = db.Column(TIMESTAMP, default=func.now())
    user = db.relationship(User)

    def __repr__(self):
        return "{}".format(self.name)

class Story(db.Model):

    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    text = db.Column(LONGTEXT)
    thumbnail = db.Column(db.String(512), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    hits = db.Column(db.Integer, default=0)
    create_time = db.Column(TIMESTAMP, default=func.now())
    user = db.relationship(User)
    tag = db.relationship(Tag)
    person = db.relationship(Person)
    topic = db.relationship(Topic)

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
