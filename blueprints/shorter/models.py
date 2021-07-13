from blueprints import db
from datetime import datetime as dt


class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_url = db.Column(db.Text)
    short_url = db.Column(db.Text)
    created = db.Column(db.DateTime, default=dt.now().replace(microsecond=0))
    creator = db.Column(db.Text)
