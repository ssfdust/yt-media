from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditorField
from jinja2 import Markup
from flask_admin import form
from wtforms import TextAreaField
from utils import gen_hash_filename
from models import User, Topic, Person, Tag, Story, Comment
from ext import admin, db
import os

file_path = os.path.join(os.path.dirname(__file__), 'uploads')

class TopicView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.thumbnail:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.thumbnail)))

    form_excluded_columns = ['create_time', 'user']
    column_exclude_list = ['user']
    column_formatters = {
        'thumbnail': _list_thumbnail
    }
    form_overrides = {
        'description': TextAreaField
    }

    form_extra_fields = {
        'thumbnail': form.ImageUploadField('thumbnail',
                                      base_path=file_path,
                                      namegen=gen_hash_filename,
                                      thumbnail_size=(100, 100, True))
    }

class TagView(ModelView):
    form_excluded_columns = ['create_time', 'user']
    column_exclude_list = ['user']
    form_overrides = {
        'description': TextAreaField
    }

class UserView(ModelView):
    form_excluded_columns = ['create_time']
    form_choices = {
        'flag': [
            (1, '普通用户'),
            (2, '管理员'),
        ]
    }
    form_overrides = {
        'description': TextAreaField
    }

class StoryView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.thumbnail:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.thumbnail.decode('utf-8'))))

    create_template = 'edit.html'
    edit_template = 'edit.html'
    form_overrides = {
        'text': CKEditorField,
        'description': TextAreaField
    }
    form_excluded_columns = ['create_time', 'user', 'hits']
    column_exclude_list = ['user']
    column_formatters = {
        'thumbnail': _list_thumbnail
    }

    form_extra_fields = {
        'thumbnail': form.ImageUploadField('thumbnail',
                                      base_path=file_path,
                                      namegen=gen_hash_filename,
                                      thumbnail_size=(100, 100, True))
    }

class CommentView(ModelView):
    form_excluded_columns = ['create_time']
    form_overrides = {
        'comment': TextAreaField
    }


admin.add_view(UserView(User, db.session))
admin.add_view(TagView(Tag, db.session))
admin.add_view(TopicView(Person, db.session))
admin.add_view(TopicView(Topic, db.session))
admin.add_view(CommentView(Comment, db.session))
admin.add_view(StoryView(Story, db.session))
