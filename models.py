"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


def connect_db(app):
    """ Connect to database. """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User. """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False,
                          default='https://hips.hearstapps.com/countryliving.cdnds.net/17/47/1511194376-cavachon-puppy-christmas.jpg')

    # posts = db.relationship('Post')

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name}>"


class Post(db.Model):
    """ Post. """

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False,
                           server_default=db.func.now())
    userid = db.Column(db.Integer,
                       db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='posts')

# For style improvements and tracking differences
    # id = db.Column(
    #     db.Integer,
    #     primary_key=True,
    #     autoincrement=True)
    # title = db.Column(
    #     db.String(50),
    #     nullable=False)
    # content = db.Column(
    #     db.Text,
    #     nullable=False)
    # created_at = db.Column(
    #     db.DateTime(timezone=True),
    #     nullable=False,
    #     server_default=db.func.now())
    # userid = db.Column(
    #     db.Integer,
    #     db.ForeignKey('users.id'),
    #     nullable=False)

    # user = db.relationship('User', backref='posts')
