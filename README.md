# Flask-Authlib

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

![alt text](screenshots/login.PNG "Title")

<p style="text-align:center;">
<small>Login page at /login</small>
</p>

![alt text](screenshots/register.PNG "Title")
<p style="text-align:center;">
<small>Register page at /register</small>
</p>

Abduaziz Ziyodov