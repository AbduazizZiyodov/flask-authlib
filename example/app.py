from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_authlib import Auth


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)

config = {
    "LOGIN_BTN": "btn-danger",
    "REGISTER_BTN": "btn-primary",

    "LOGIN_PAGE_TITLE": "Administration",
    "REGISTER_PAGE_TITLE": "Administration"
}

auth = Auth(app=app, db=db, template_config=config)
auth.init()


@app.route('/')
def home_page():
    return {'message': 'Hi, bro 😁'}

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')