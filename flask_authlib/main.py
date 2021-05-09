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
from flask_authlib.exceptions import ConfigError
from flask_authlib.utils import load_template_config

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
                 app: Flask = None,
                 db: SQLAlchemy = None,
                 home_page: str = '/',
                 login_url: str = '/login',
                 register_url: str = '/register',
                 logout_url: str = '/logout',
                 template_config: dict = None
                 )->None:
        # Setting app and db
        self.app = app
        self.db = db
        # Set template config
        self.template_config = template_config
        self.__set_template_config(config=self.template_config)
        # Settings url rules
        self.__set_rules(login_url, register_url, logout_url, home_page)
        self.__setup()

    def init(self):
        """
        Method for initalization.
        auth = Auth(app, db)
        auth.init()
        """
        if self.app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:':
           raise ConfigError('PLEASE SET DATABASE URI !!!')
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
        # Setting Auth Alert Messages
        self.__set_alerts()
        # Login view: auth -> login_form
        self.login_manager.login_view = 'auth.login_form'
        # Alert message category
        self.login_manager.login_message_category = "info"
        # Defalt user loader

        @self.login_manager.user_loader
        def load_user(user_id):
            return self.User.query.get(user_id)

    def __set_template_config(self, config: dict = None) -> None:
        default_config = load_template_config()
        cfg = {}

        if config is None:
            self.template_config = default_config
        else:
            for i in default_config.keys():
                if i in config:
                    cfg[i] = config[i]
                else:
                    cfg[i] = default_config[i]
            self.template_config = cfg

    def __get(self):
        bcrypt = Bcrypt(self.app)
        login_manager = LoginManager(self.app)

        return bcrypt, login_manager

    def __set_alerts(self):
        # Alert messages
        self.ALERTS = get_alerts()

        self.EMAIL_ALERT = self.ALERTS['EMAIL_ALERT']
        self.USERNAME_ALERT = self.ALERTS['USERNAME_ALERT']
        self.PASSWORD_LENGTH = self.ALERTS['PASSWORD_LENGTH']
        self.REGISTER_SUCCESS = self.ALERTS['REGISTER_SUCCESS']

        self.LOGIN_FAIL = self.ALERTS['LOGIN_FAIL']

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

    def __add_auth_depences(self):
        auth.add_url_rule(rule=self.LOGIN_URL,
                          methods=['GET'],
                          view_func=self.__get_login_form())

        auth.add_url_rule(rule=self.REGISTER_URL,
                          methods=['GET'],
                          view_func=self.__get_register_form())

        auth.add_url_rule(rule='/auth/register',
                          methods=['POST'],
                          view_func=self.__get_register_controller())

        auth.add_url_rule(rule="/auth/login",
                          methods=['POST'],
                          view_func=self.__get_login_controller())

        auth.add_url_rule(rule=self.LOGOUT_URL,
                          view_func=self.__get_logout_controller())

    def __get_login_form(self):
        def login_form():

            if current_user.is_authenticated:
                return redirect(self.HOME_PAGE)

            return render_template('login.html',
                                   title='Login',
                                   cfg=self.template_config,
                                   reg=self.REGISTER_URL)

        return login_form

    def __get_register_form(self):
        def register_form():

            if current_user.is_authenticated:
                return redirect(self.HOME_PAGE)
            return render_template('register.html',
                                   title='Register',
                                   cfg=self.template_config,
                                   log=self.LOGIN_URL)

        return register_form

    def __get_login_controller(self):
        def login():
            username, password = request.form['username'], request.form[
                'password']

            if current_user.is_authenticated:
                return redirect(self.HOME_PAGE)

            user = self.User.query.filter_by(username=username).first()

            if user and self.bcrypt.check_password_hash(
                    user.password_hash, password):
                login_user(user)

                return redirect(self.HOME_PAGE)
            else:
                flash(self.LOGIN_FAIL, 'danger')
                return redirect(self.LOGIN_URL)

        return login

    def __get_register_controller(self):
        def register():
            email, username, password = request.form['email'], request.form[
                'username'], request.form['password']

            if current_user.is_authenticated:
                return redirect(self.HOME_PAGE)

            elif self.User.query.filter_by(email=email).first():
                flash(self.EMAIL_ALERT, 'danger')
                return redirect(self.REGISTER_URL)

            elif self.User.query.filter_by(username=username).first():
                flash(self.USERNAME_ALERT, 'danger')
                return redirect(self.REGISTER_URL)

            elif len(password) < 8:
                flash(self.PASSWORD_LENGTH, 'warning')
                return redirect(self.REGISTER_URL)

            else:
                hashed_password = self.bcrypt.generate_password_hash(
                    password).decode('utf-8')
                user = self.User(email=email,
                                 username=username,
                                 password_hash=hashed_password)

                user.insert()
                flash(self.REGISTER_SUCCESS, 'success')
                return redirect(self.LOGIN_URL)

        return register

    def __get_logout_controller(self):
        def logout():
            logout_user()
            return redirect(self.HOME_PAGE)

        return logout
