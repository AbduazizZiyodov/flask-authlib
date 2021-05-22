# **Flask-Authlib** 🔐

<img src="https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&type=6&v=1.3.1&x2=0" alt="PyPI version" height="18">

<hr>

Flask-Authlib - authentication library for Flask Web Framework.

Advantages:

- Templates: login , register
- Default `user` Model
- View Functions

# Install

By using `pip`:

```bash
$ pip install flask-authlib
```

# Simple Usage

- Import `Flask` from `flask`
- Import `SQLAlchemy` from `flask_sqlalchemy`
- Import `Auth` from `flask_authlib`

Code Sample:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_authlib import Auth
```

Define your `app` and `db`. Create auth var from `Auth` class and call `init()` method:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_authlib import Auth

app = Flask(__name__)
db = SQLAlchemy(app)

auth = Auth(app=app, db=db)
auth.init()

# simple route
@app.route('/')
def home_page():
    return {'message': 'Hi, bro 😁'}
```

Run your backend:

```bash
$ export FLASK_APP=<app> && export FLASK_ENV=development
$ flask run --reload
```

**Screenshots:**

![LOGIN](screenshots/login.PNG)
Login page at `/login`

![REGISTER](screenshots/register.PNG)
Register page at `/register`

# **Advanced Usage**

> You can change urls

**Defaults**

- Home page - `/`
- Login page - `/login`
- Register page - `/register`
- Logout url - `/logout`

Write your urls before calling `init()` method:

```python
...

auth = Auth(app=app, db=db, login_url='/mylogin',
            register_url='/myreg', logout_url='/myexit',
            home_page='/')
auth.init()
...
```

> You can set your own template config!

You can change:

- Button color on forms
- Form title at login and register page
- All labels like Username.. email ...
- Text in button.

**Default template config**

```json

config = {
        "LOGIN_BTN": "btn-success",
        "REGISTER_BTN": "btn-warning",

        "LOGIN_BTN_TEXT": "Login",
        "REGISTER_BTN_TEXT": "Register",

        "LOGIN_PAGE_TITLE": "Login",
        "REGISTER_PAGE_TITLE": "Register",

        "LOGIN_LABEL_USERNAME": "Username",
        "LOGIN_LABEL_PASSWORD": "Password",
        "REGISTER_LABEL_USERNAME": "Username",
        "REGISTER_LABEL_PASSWORD": "Password",
        "REGISTER_LABEL_EMAIL": "Email address"
}
```

_p.s btn colors based on bootstrap classes_

Setting your config:

```python
...
my_config = {
        "LOGIN_BTN": "btn-danger",
        "REGISTER_BTN": "btn-primary",

        "LOGIN_PAGE_TITLE": "Admin",
        "REGISTER_PAGE_TITLE": "Admin"
}
auth = Auth(app=app, db=db, template_config=my_config)
auth.init()
...
```

> If some settings are not entered, they remain as default

**Screenshots:**

> ![LOGIN](screenshots/login_2.PNG)
> Login page

<hr>

> ![REGISTER](screenshots/register_2.PNG)
> Register page

# **Running Example** 🚀

### First way

> Required `docker`

Project directory have:

- dockerfile
- docker_compose.yml

For running this you have to type this command:

```bash
$ docker-compose up
```

Screenshot:

![DOCKER](screenshots/docker.PNG)

## **Second way**

Clone this repo:

```bash
$ git clone https://github.com/AbduazizZiyodov/flask-authlib.git
```

Navigate to `/example`:

```bash
$ cd example/
```

Install all required packages:

```bash
$ pip install -r requirements.txt
```

Run development server:

- `$ python app.py` or
- `$ gunicorn app:app` or
- `$ export FLASK_APP=app && flask run --reload`

Enjoy 😅

# **JWT**

> v1.3.1

Setup JWT authentication for your API with auth0!

Example:

```python
from flask import Flask
from flask_authlib import JWT

app = Flask(__name__)
jwt = JWT(app=app, AUTH0_DOMAIN='',API_AUDIENCE='')

required = jwt.get_requires_auth_decorator()

@app.route('/', methods=['GET'])
@required('read:data')
def home(token):
    return {"data": "secret"}

```

- Import `JWT` from this library
- Define your app
- Create jwt var from JWT class and set some vars.
  > Params:
  > **AUTH0_DOMAIN**: your domain for auth0:
  > ![DOMAIN](screenshots/auth0_domain.PNG)
  > "abduaziz.us.auth0.com"
  > **API_AUDINCE**: your api idenf. for auth0:
  > ![AUDINCE](screenshots/audince.PNG)
  > "test_api"
  > create example of decorator by calling `get_requires_auth_decorator()` method

```python
@requires(permission:str)
```

> If permission in auth token , this view will be send success response , else 401😅

Before doing these , you have to create user permissions from your **API**:

![AUDINCE](screenshots/audince.PNG)

> `read:data` permission

For testing ,you should register new user and get token from response:

![LOGIN_URI](screenshots/login_uri.PNG)

> LOGIN_URI:

```
https://{{AUTH0_DOMAIN}}/authorize?
audience={{API_AUDINCE}}&response_type=token&
client_id={{CLIENT_ID}}&redirect_uri={{REDIRECT_URI}}
```

* `CLIENT_ID` - you can get it from your page of API.
* `REDIRECT_URI` - you can set it from API settings

After adding new user , navigate user management page and assign permissions to your user:

![PERM](screenshots/user_perm.PNG)

> logout_uri: `{AUTH0_DOMAIN}/logout`

Next , login again and you will get permission based jwt token:

![TOKEN](screenshots/jwt.PNG)
🎉

## **Test it !**

Send request without auth token:

![401](screenshots/401.PNG)

Send request with auth token:

![OK](screenshots/jwt_success.PNG)
✅ Success!

**Author: Abduaziz Ziyodov**
