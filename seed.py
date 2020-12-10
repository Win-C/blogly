"""Seed file to make sample data for blogly db."""

from models import db, connect_db, User, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add users
u1 = User(first_name="Sylvia", last_name="Plath", image_url="https://media.poetryfoundation.org/uploads/media/default/0001/16/9335c30d45c8a838017ed7508083bc341aa50e73.jpeg?w=690&h=&fit=max&690")
u2 = User(first_name="Claire", last_name="Casey")
u3 = User(first_name="Winnie", last_name="Chou")

# Add posts
p1 = Post(title="Post 1!", content="test test yay", userid="2" )
p2 = Post(title="Post 2!", content="test test yay", userid="2" )
p3 = Post(title="Post 3!", content="test test yay", userid="2" )
p4 = Post(title="Post 4!", content="test test yay", userid="1" )
p5 = Post(title="Post 5!", content="test test yay", userid="3" )

# Add new objects to session, so they'll persist
db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)

# Commit--otherwise, this never gets saved!
db.session.commit()