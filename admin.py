from flask import url_for, redirect, request
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditorField
from jinja2 import Markup
from flask_login import current_user, login_user, logout_user
from flask_admin import form, expose, helpers, AdminIndexView
from wtforms import form as wtfform, fields, validators, TextAreaField
from utils import gen_hash_filename
from models import User, Topic, Person, Tag, Story, Comment
from ext import admin, db
import os

file_path = os.path.join(os.path.dirname(__file__), 'uploads')

class LoginForm(wtfform.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None or user.flag != 2:
            raise validators.ValidationError('Invalid user')

        if not user.check_password(self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.query.filter_by(username=self.login.data).first()

class AuthAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(AuthAdminIndexView, self).index()

    @expose('/login/', methods=['GET', 'POST'])
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(AuthAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))

class TopicView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.thumbnail:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.thumbnail)))

    def is_accessible(self):
        return current_user.is_authenticated

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

    def is_accessible(self):
        return current_user.is_authenticated

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

    def is_accessible(self):
        return current_user.is_authenticated

class StoryView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.thumbnail:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.thumbnail)))

    def is_accessible(self):
        return current_user.is_authenticated

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
        'thumbnail': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      namegen=gen_hash_filename,
                                      thumbnail_size=(100, 100, True))
    }

class CommentView(ModelView):
    form_excluded_columns = ['create_time']
    form_overrides = {
        'comment': TextAreaField
    }

    def is_accessible(self):
        return current_user.is_authenticated


admin._set_admin_index_view(AuthAdminIndexView())
admin.add_view(UserView(User, db.session))
admin.add_view(TagView(Tag, db.session))
admin.add_view(TopicView(Person, db.session))
admin.add_view(TopicView(Topic, db.session))
admin.add_view(CommentView(Comment, db.session))
admin.add_view(StoryView(Story, db.session))
