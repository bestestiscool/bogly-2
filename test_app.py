# test_app.py
import unittest
from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from config import TestConfig 


app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'user123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


class FlaskBloglyTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test variables and initialize app."""
        app.config.from_object(TestConfig)
        self.client = app.test_client()

        # Bind the app to the current context
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down test variables."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_redirect(self):
        """Test index route redirects to list of users."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users', response.location)

    def test_list_users(self):
        """Test users listing."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn('All Users', response.data.decode())

    def test_add_user(self):
        """Test user creation page."""
        response = self.client.get('/users/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Add User', response.data.decode())

    def test_user_creation(self):
        """Test creating a new user."""
        response = self.client.post('/users/new', data=dict(
            first_name='Test',
            last_name='User',
            image_url='http://example.com/image.png'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test User', response.data.decode())

if __name__ == '__main__':
    unittest.main()
