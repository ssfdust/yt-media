from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from models import Person, Story, Tag, Topic, Comment

class PersonSchema(ModelSchema):
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Person

class StorySchema(ModelSchema):
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    tag = fields.String(attribute='tag.name', default=None)
    topic = fields.String(attribute='topic.name', default=None)
    person = fields.String(attribute='person.name', default=None)

    class Meta:
        model = Story

class TagSchema(ModelSchema):
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Tag

class TopicSchema(ModelSchema):
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Topic

class CommentSchema(ModelSchema):
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    commenter = fields.String(attribute='user.username')

    class Meta:
        model = Comment
