from os import urandom

from flask import Flask
from flask import flash
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template

from flask_sqlalchemy import SQLAlchemy

from flask_authlib.utils import get_alerts
from flask_authlib.auth.models import get_models

from flask_bcrypt import Bcrypt

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import LoginManager


auth = Blueprint('auth', __name__, template_folder='pages')


class Auth(object):
    """

    Auth
    `app` - Your Flask Application
    `db` - your db -> (SQLAlchemy) default is None

    `home_page` - home page url default `/`
    `login_url` - login page url default `/login`
    `register_url` - register page url default `/register`
    `logout_url` - logout router rule default `/logout`

    app = Flask(__name__)
    db = SQLAlchemy(app)
    auth = Auth(app=app, db=db)

    """

    def __init__(self,
                 app: Flask,
                 db=None,
                 home_page='/',
                 login_url='/login',
                 register_url='/register',
                 logout_url='/logout') -> None:
        # Setting app and db
        self.app = app
        self.db = db

        # Settings url rules
        self.__set_rules(login_url, register_url, logout_url, home_page)
        self.__setup()

    def init(self):
        """
        Method for initalization.
        auth = Auth(app, db)
        auth.init()
        """
        try:
            # Setting Application secret key
            self.__add_secret_key()
            # Adding all auth depences
            self.__add_auth_depences()
            self.app.register_blueprint(auth)

        except AssertionError:
            pass

    def __setup(self):
        # Check db if exist ...
        self.db = self.__check_db()
        # Get User Database Model
        self.User = get_models(self.db)
        # Create Tables using This Model
        self.__create_tables()
        # Setting bcrypt and login_manager for current app
        self.bcrypt, self.login_manager = self.__get()
        # Login view: auth -> login_form
        self.login_manager.login_view = 'auth.login_form'
        # Alert message category
        self.login_manager.login_message_category = "info"
        # Defalt user loader

        @self.login_manager.user_loader
        def load_user(user_id):
            return self.User.query.get(user_id)

    def __get(self):
        bcrypt = Bcrypt(self.app)
        login_manager = LoginManager(self.app)

        return bcrypt, login_manager

    def __set_rules(self, login_url, register_url, logout_url, home_page):
        self.LOGIN_URL = login_url
        self.REGISTER_URL = register_url
        self.LOGOUT_URL = logout_url

        self.HOME_PAGE = home_page

    def __check_db(self):
        if self.db is None:
            return SQLAlchemy(self.app)
        else:
            return self.db

    def __add_secret_key(self):
        if self.app.secret_key is None:
            self.app.secret_key = urandom(32)

    def __create_tables(self):
        self.db.create_all()