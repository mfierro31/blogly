"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'chickenzarecool31'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def direct_to_homepage():
    """Redirects to real homepage"""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Lists all users in the db"""
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/users/new')
def show_form():
    """Shows add user form"""
    return render_template('add_user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    first = request.form['first']
    last = request.form['last']
    image = request.form['image']

    new_user = User(first_name=first, last_name=last, image_url=image)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)