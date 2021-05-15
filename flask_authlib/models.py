from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

def get_models(db: SQLAlchemy):
    class User(db.Model, UserMixin):
        __tablename__ = 'Users'

        def __init__(self, username, email, password_hash):
            self.username = username
            self.email = email
            self.password_hash = password_hash

        id = Column(Integer, primary_key=True)
        username = Column(String, nullable=False)
        email = Column(String, nullable=False)
        password_hash = Column(String, nullable=False)

        def insert(self):
            db.session.add(self)
            db.session.commit()

    return User
