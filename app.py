"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = "Shhhhhh!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.drop_all()
db.create_all()

debug = DebugToolbarExtension(app)


@app.route('/')
def home():
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
    image_url = request.form['image_url'] if request.form['image_url'] else None

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

    user = User.query.get_or_404(user_id)

    # TO DO: check if we can just input 'user' here
    return render_template('user_detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_user_edit(user_id):
    """ Show the edit page for a specific user and buttons to return to
        the detail page for a user and save button that updates the user
     """

    user = User.query.get_or_404(user_id)

    return render_template('user_edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def show_edit_form(user_id):
    """ Process the edit form and returns the user to the /users page """

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """ Delete the user """

    user = User.query.filter_by(id=user_id).delete()

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """ Show new post form to add a post for that user """

    user = User.query.get_or_404(user_id)

    return render_template('new_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """ Handle new post form; add post and redirect to the
        user detail page """

    title = request.form['title']
    content = request.form['content']

    user = User.query.get_or_404(user_id)

    new_post = Post(title=title,
                    content=content,
                    userid=user.id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{ user.id }')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ Show a post based on post_id """

    post = Post.query.get_or_404(post_id)

    return render_template('post_detail.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def show_post_edit(post_id):
    """ Show a edit form for post based on post_id """

    post = Post.query.get_or_404(post_id)

    return render_template('post_edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """ Handle edit post form; update post and redirect to the
        post view """

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f'/posts/{ post.id }')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """ Delete the post """
    user_id = Post.query.get_or_404(post_id).userid

    Post.query.filter_by(id=post_id).delete()

    db.session.commit()

    return redirect(f'/users/{user_id}')
