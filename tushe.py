# -*- coding:utf-8 -*-
from app import app, login_manager
from flask.ext.admin import Admin
from flask.ext.admin.contrib.fileadmin import FileAdmin
from views import light_cms
from wc import wc
from admin_views import UserView, IndexView, GeneralView
from models import User, Image, Gallery
import settings


login_manager.init_app(app)

app.register_blueprint(light_cms)
app.register_blueprint(wc)

admin = Admin(app, name="{}后台管理".format(settings.SITE_NAME), index_view=IndexView(endpoint='admin'))
admin.add_view(UserView(User, name='用户'))
admin.add_view(FileAdmin(settings.UPLOAD_FOLDER, settings.UPLOAD_URL, name='媒体文件'))
admin.add_view(GeneralView(Image, name='图片'))
admin.add_view(GeneralView(Gallery, name='图册'))
