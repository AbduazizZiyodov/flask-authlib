from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy


def get_user_model(db: SQLAlchemy, table_name: str):
    class User(db.Model, UserMixin):
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String, nullable=False)
        email = db.Column(db.String, nullable=False)
        password_hash = db.Column(db.String, nullable=False)
        admin = db.Column(db.Boolean, default=False)

        def is_admin(self) -> bool:
            return self.admin

        def insert(self) -> None:
            db.session.add(self)
            db.session.commit()

    return User
