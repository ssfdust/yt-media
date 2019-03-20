from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields, Schema
from models import Person, Story, Tag, Topic, Comment
from ext import rest_api

@rest_api.definition('login_info')
class LoginSchema(Schema):
    username = fields.String(description='用户名')
    password = fields.String(description='密码')

@rest_api.definition('args')
class BaseArgSchema(Schema):
    number = fields.Int(default=1, dump_to='num', description='最大返回数量')
    id = fields.Int(default=None, description='指定内容的ID')

@rest_api.definition('tag_args')
class TagArgSchema(BaseArgSchema):
    is_great = fields.Boolean(default=False, description='是否为精选内容<br>'
                                                        ' 0为否 1为是 默认为全部')

@rest_api.definition('story_args')
class StoryArgSchema(Schema):
    name = fields.String(description='故事名称')
    hot = fields.Boolean(description='是否按照热门内容排序')
    person_id = fields.Int(description='人物ID')
    tag_id = fields.Int(description='标签ID')
    topic_id = fields.Int(description='主题ID')

class LoginMsgSchema(Schema):
    username = fields.String(description='用户名')
    code = fields.Int(description='返回码 成功为0 找不到为404 无权访问为403')
    msg = fields.String(description='信息')

class MsgSchema(Schema):
    code = fields.Int(description='返回码 成功为0 找不到为404 无权访问为403')
    msg = fields.String(description='信息')

class UserInfoSchema(Schema):
    username = fields.String(description='用户名')
    flag = fields.Int(description='标记 管理员为2 普通用户为1')

class InfoRetSchema(Schema):
    code = fields.Int(description='返回码 成功为0 找不到为404 无权访问为403')
    userinfo = fields.Nested(UserInfoSchema)

@rest_api.definition('Person')
class PersonSchema(ModelSchema):
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Person

class BaseRetSchema(Schema):
    code = fields.Int(description='返回码 成功为0 无失败情况')
    total = fields.Int(description='返回的条目数量')

class PersonRetSchema(BaseRetSchema):
    data = fields.Nested(PersonSchema(many=True))

@rest_api.definition('Story')
class StorySchema(ModelSchema):
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    tag = fields.String(attribute='tag.name', default=None)
    topic = fields.String(attribute='topic.name', default=None)
    person = fields.String(attribute='person.name', default=None)
    number = fields.Int(default=1, dump_to='num', description='最大返回数量')

    class Meta:
        model = Story

class StoryRetSchema(BaseRetSchema):
    data = fields.Nested(StorySchema(many=True))

class StoryItemSchema(BaseRetSchema):
    data = fields.Nested(StorySchema())

@rest_api.definition('Tag')
class TagSchema(ModelSchema):
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Tag

class TagRetSchema(BaseRetSchema):
    data = fields.Nested(TagSchema(many=True))

@rest_api.definition('Topic')
class TopicSchema(ModelSchema):
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Topic

class TopicRetSchema(BaseRetSchema):
    data = fields.Nested(TopicSchema(many=True))

@rest_api.definition('Comment')
class CommentSchema(ModelSchema):
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    commenter = fields.String(attribute='user.username')

    class Meta:
        model = Comment
