# **JWT modules' customization**

`flask_authlib.JWT` allows you to create your own settings object and use it. You should only create a class based on `flask_authlib.JwtConfig`, make your changes and it's ready for use.

### **Basic app and configuration**

Create your flask app and import the `JwtConfig` object from `flask_authlib` for customization:

```python hl_lines="4 5"
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_authlib import AuthManager
from flask_authlib import JwtConfig

app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"

auth = AuthManager(app, db)

app.add_url_rule(rule="/",view_func=lambda : "Hello World!")
```

Define your settings class:

```python

class MySettings(JwtConfig):
    pass

```

Apply your settings:

```python
auth = JWT(app,db,settings=MySettings)
```

### **URLs customization**

```python
class MySettings(JwtConfig):
    LOGIN_URL:str = "/api/login"
    REGISTER_URL:str = "api/register"
```

### **Changing `TABLENAME`**

```python
class MySettings(JwtConfig):
    TABLENAME:str = "accounts"
```

### **Minimum password length**

```python
class MySettings(JwtConfig):
    MIN_PASSWORD_LENGTH:int = 12
```

### **Custom token lifetime**

!!! info "Token Lifetime"

    All **jwt** tokens have an expiration time. This expiration time is set by the `server-side (in the encoding process). If a token has expired, users can't use it on *protected* routes.

In this library, you can set your token lifetime.

```python
class MySettings(JwtConfig):
    TOKEN_LIFETIME: int = 60*30 # seconds
```

> 60x30 = 1800 seconds = 0.5 hour

### **User Info**

In the `Advanced usage of JWT` sections, I wrote that you can get user credentials by its `JWT` token easily. But, there are some cases that we should not do this. For example, if users changed their profile(username, email), the credentials do not match with data on the database.

```python
class MySettings(JwtConfig):
    USER_INFO_IN_JWT:bool = False
```

Now, we can get only `user_id` from **jwt** token ("sub") and our `jwt_requires` decorator(which allows you to get current user) fetch user from the database according to its `user_id`.

> If you set this param is `False`, you can still get `user` like a previous guide.

### **Alert Messages**

As you know, if the authentication process raises any exceptions, the server returns `401` response with a status code and error message. For changing this you should create another object for alerts.

```python hl_lines="3 7"
from flask_authlib import Alerts

class MyAlerts(Alerts):
    LOGIN_FAIL:str = "..."

class MySettings(JwtConfig):
    alerts:Alert = MyAlerts
```

### **JwtConfig's Defaults**

```python
class JwtConfig:
    LOGIN_URL: str = "/login"
    REGISTER_URL: str = "/register"

    TABLENAME: str = "users"
    MIN_PASSWORD_LENGTH: int = 8

    TOKEN_LIFETIME: int = 60*60  # seconds
    SECRET_KEY: str = secrets.token_hex()

    USER_INFO_IN_JWT:bool = True

    alerts: Alerts = Alerts

    user_schema:User = User
```
