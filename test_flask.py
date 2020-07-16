from unittest import TestCase

from app import app
from models import db, User

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
            self.assertIn('<h1>Create a new user</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first": "User", "last": "2", "image": "https://hips.hearstapps.com/digitalspyuk.cdnds.net/16/41/1476281167-gamora-guardians-of-the-galaxy.jpg?crop=0.512xw:1.00xh;0.141xw,0&resize=480:*"}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/2">User 2</a></li>', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>User 1</h1>', html)
