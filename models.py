"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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
                          default='')

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name}>"

    def is_not_same_or_empty(self, value, col_name):
        """ Checks if value passed in already exists in the record or 
            is an empty string
            Returns: False, if exists in record or ''
                     True, otherwise
        """
        # Note: may need to mock a db to test function, come back to this

        if (self.col_name is value) or (self.col_name == ''):
            return False

        return True
