# Flask-Authlib

[![PyPI version](https://badge.fury.io/py/Flask-Authlib.svg)](https://badge.fury.io/py/Flask-Authlib)

<hr>

Flask-Authlib - authentication library for Flask Web Framework.

- Templates: login , register
- User Model
- View Functions

# Install

By using `pip`:

```bash
$ pip install flask-authlib
```

# Usage

- Firstly, import `Flask` from `flask`
- Secondly, import `SQLAlchemy` from `flask_sqlalchemy`
- Lastly, import `Auth` from `flask_authlib`

Code:

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

Screenshot:

![LOGIN](screenshots/login.PNG)
<small>Login page at /login</small>

![REGISTER](screenshots/register.PNG)
<small>Register page at /register</small>

# Advanced Usage

> You can change urls

**Defaults**

- Login page - `/login`
- Register page - `/register`
- Logout url - `/logout`
- Home page - `/`

Write your urls before calling `init()` method at `Auth` class:

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

- Button colors at login and register page
- Title at login and register page
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

_p.s login-btn colors based on bootstrap classes_

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

p.s if the some settings are not entered, they will remain in their state.

Screenshot:

![LOGIN](screenshots/login_2.PNG)
<small>Login page with own config</small>

![REGISTER](screenshots/register_2.PNG)
<small>Register page with own config</small>


Author: Abduaziz Ziyodov
