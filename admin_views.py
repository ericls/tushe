# -*- coding: utf-8 -*-

from flask import redirect, url_for
from flask_admin.contrib.mongoengine import ModelView
from flask.ext.admin import AdminIndexView
from app import login


class IndexView(AdminIndexView):

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('light-cms.user_login'))

    def is_accessible(self):
        if not login.current_user.is_authenticated():
            return False
        return login.current_user.is_admin


class UserView(ModelView):

    column_labels = dict(
        username='用户名',
        password_hash='密码哈希',
        active='可用',
        is_admin='管理员'
    )

    column_filters = ('username', 'active', 'is_admin')
    column_list = ('username', 'active', 'is_admin', 'email')

    form_create_rules = ('username', 'password', 'active', 'is_admin', 'email')
    form_edit_rules = form_create_rules

    def is_accessible(self):
        if not login.current_user.is_authenticated():
            return False
        return login.current_user.is_admin


class GeneralView(ModelView):

    def is_accessible(self):
        if not login.current_user.is_authenticated():
            return False
        return login.current_user.is_admin
