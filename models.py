"""Models for Blogly."""
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