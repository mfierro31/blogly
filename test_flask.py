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

class UsersTestCase(TestCase):
    """Testing all the functionality associated with users"""
    def setUp(self):
        """Add sample user"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name='User', last_name='1', image_url='https://vignette.wikia.nocookie.net/marvelcinematicuniverse/images/6/63/97d1d9f934a350cee765c5ac1a466605.jpg/revision/latest/top-crop/width/360/height/360?cb=20190527184444')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled session transactions"""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User 1', html)

    def test_add_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="mt-4">Create a new user</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first": "User", "last": "2", "image": "https://hips.hearstapps.com/digitalspyuk.cdnds.net/16/41/1476281167-gamora-guardians-of-the-galaxy.jpg?crop=0.512xw:1.00xh;0.141xw,0&resize=480:*"}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User 2</a></li>', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>User 1</h1>', html)

    def test_show_edit_user_form(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="mt-3">Edit User 1</h1>', html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first": "Person", "last": "3", "image": "https://vignette.wikia.nocookie.net/rickandmorty/images/7/70/1490478881683.jpg/revision/latest?cb=20190129225851"}
            resp = client.post(f'/users/{self.user_id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<li><a href="/users/{self.user_id}">Person 3</a></li>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'<li><a href="/users/{self.user_id}">User 1</a></li>', html)

class PostsTestCase(TestCase):
    """Testing all the functionality associated with posts"""
    def setUp(self):
        """Add sample post and sample user"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name='User', last_name='1', image_url='https://vignette.wikia.nocookie.net/marvelcinematicuniverse/images/6/63/97d1d9f934a350cee765c5ac1a466605.jpg/revision/latest/top-crop/width/360/height/360?cb=20190527184444')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        post = Post(title='Title 1', content='Content 1', user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled session transactions"""
        db.session.rollback()

    def test_list_posts_on_homepage(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<li><a href="/posts/{self.post_id}">Title 1</a></li>', html)

    def test_list_posts_on_user_page(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<li><a href="/posts/{self.post_id}">Title 1</a></li>', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Content 1</p>', html)

    def test_show_add_post_form(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="mt-3 mb-5">Add Post for User 1</h1>', html)

    def test_add_post(self):
        with app.test_client() as client:
            p = {"title": "Title 2", "content": "Content 2", "user_id": self.user_id}
            resp = client.post(f'/users/{self.user_id}/posts/new', data=p, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('>Title 2</a></li>', html)

    def test_edit_post_form(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="mt-3">Edit Post</h1>', html)

    def test_edit_post(self):
        with app.test_client() as client:
            p = {"title": "Title 3", "content": "Content 3"}
            resp = client.post(f'/posts/{self.post_id}/edit', data=p, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="mt-3">Title 3</h1>', html)
            self.assertIn('<p>Content 3</p>', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Title 1</a></li>', html)