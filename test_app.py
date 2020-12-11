from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """ Tests for views for Users. """

    def setUp(self):
        """ Add a sample user. """

        Post.query.delete()
        User.query.delete()

        user = User(first_name="Sylvia", last_name="Plath", image_url="")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """ Clean up any fouled transaction. """

        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<li><a href="/users/{self.user_id}">', html)

    def test_users_list(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<li><a href="/users/{self.user_id}">', html)

    def test_user_new_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('id="first-name"', html)

    def test_create_user(self):
        first_name_test = "Margaret"
        last_name_test = "Atwood"
        with app.test_client() as client:
            d = {
                "first_name": first_name_test,
                "last_name": last_name_test,
                "image_url": ""}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{first_name_test} {last_name_test}", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {
                "first_name": "Sylvia",
                "last_name": "New_Last",
                "image_url": ""}
            resp = client.post(f'/users/{self.user_id}/edit', data=d,           follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sylvia New_Last", html)


class PostViewsTestCase(TestCase):
    """ Tests for views for Posts. """

    def setUp(self):
        """ Add a sample user and a sample post. """

        Post.query.delete()
        User.query.delete()

        user = User(first_name="Sylvia", last_name="Plath", image_url=None)

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title="New Post",
                    content="test test yay",
                    userid=self.user_id)

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """ Clean up any fouled transaction. """

        db.session.rollback()

    def test_show_form(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('id="title"', html)

    def test_post_added(self):
        d = {
            "title": "Post Added",
            "content": "new test test Yay?",
            "userid": self.user_id}
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/posts/new',
                               data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Post Added', html)

    def test_post_edit(self):
        d = {
            "title": "Post Edit",
            "content": "test test yay",
            "userid": self.user_id}
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/edit',
                               data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Post Edit', html)
            self.assertIn('test test yay', html)

    def test_post_delete(self):
        with app.test_client() as client:
            print("post id=", self.post_id)
            resp = client.post(f'/posts/{self.post_id}/delete',
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('New Post', html)
            self.assertNotIn('test test yay', html)
