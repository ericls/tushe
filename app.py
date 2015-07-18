from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.bcrypt import Bcrypt
from flask.ext import login
from flask.ext.babelex import Babel
import settings

app = Flask(settings.APP_NAME)
app.config.from_object(settings)

login_manager = login.LoginManager()

app.config['BCRYPT_LOG_ROUNDS'] = 1

db = MongoEngine(app)
bcrypt = Bcrypt(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
        # Put your logic here. Application can store locale in
        # user profile, cookie, session, etc.
        return 'zh_CN'
