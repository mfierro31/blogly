"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(25), nullable=False)

    last_name = db.Column(db.String(25), default='')

    image_url = db.Column(db.Text, nullable=False, default='https://www.sackettwaconia.com/wp-content/uploads/default-profile.png')

    def __repr__(self):
        """Show info about user"""
        u = self
        return f"<User id={u.id}, first_name={u.first_name}, last_name={u.last_name}, image_url={u.image_url}>"

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')

    def __repr__(self):
        """Show info about post"""
        p = self
        return f"<Post id={p.id}, title={p.title}, content={p.content}, created_at={p.created_at}, user_id={p.user_id}>"