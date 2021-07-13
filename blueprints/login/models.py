from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from blueprints import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    admin = db.Column(db.Boolean, default=False)

    @property
    def is_admin(self):
        if self.admin:
            return True
        else:
            return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
