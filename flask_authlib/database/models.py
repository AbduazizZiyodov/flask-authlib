from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy


def get_user_model(db: SQLAlchemy, table_name: str):
    class User(db.Model, UserMixin):
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}

        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String, nullable=False)
        username = db.Column(db.String, nullable=False)
        password_hash = db.Column(db.String, nullable=False)
        is_admin = db.Column(db.Boolean, default=False)

        def insert(self) -> None:
            db.session.add(self)
            db.session.commit()

        def to_dict(self):
            columns: list[str] = self.__table__.columns.keys()

            return {
                key: getattr(self, key)
                for key in columns
            }

    return User
