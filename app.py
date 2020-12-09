"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "Shhhhhh!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)


@app.route('/')
def home_redirect():
    """ Redirect user to list of users """
    return redirect('/users')


@app.route('/users')
def show_users():
    """ Get list of users and show all users. """

    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/new')
def show_add_form():
    """ Show form to create user. """

    return render_template('user_create.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    """ Given form inputs, create a new user instance and redirect to /users """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """ Show detail information about a specific user and buttons to edit/
    delete user """

    user = User.query.get(user_id)

    # TO DO: check if we can just input 'user' here
    return render_template('user_detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_user_edit(user_id):
    """ Show the edit page for a specific user and buttons to return to
        the detail page for a user and save button that updates the user
     """

    user = User.query.get(user_id)

    return render_template('user_edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def show_edit_form(user_id):
    """ Process the edit form and returns the user to the /users page """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get(user_id)

    if user.is_not_same_or_empty(first_name, 'first_name'):
        user.first_name = first_name

    if user.is_not_same_or_empty(last_name, 'last_name'):
        user.last_name = last_name

    if user.is_not_same_or_empty(image_url, 'image_url'):
        user.image_url = image_url

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def show_user_edit(user_id):
    """ Delete the user """

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
