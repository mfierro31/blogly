"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users=users)

@app.route('/users/new')
def show_add_user_form():
    """Shows add user form"""
    return render_template('add_user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Adds new user if required field is met"""
    first = request.form['first']
    last = request.form['last']
    image = request.form['image']
    image = image if image else None

    if not first:
        flash('First Name is required')
        return redirect('/users/new')
    else:
        new_user = User(first_name=first, last_name=last, image_url=image)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/users')

@app.route('/users/<int:user_id>')
def show_details(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_changes(user_id):
    user = User.query.get_or_404(user_id)

    first = request.form['first']
    last = request.form['last']
    image = request.form['image']
    no_last = request.form.get('last-check')
    no_image = request.form.get('image-check')

    if first:
        user.first_name = first
        db.session.add(user)

    if last:
        user.last_name = last
        db.session.add(user)

    if no_last:
        user.last_name = ''
        db.session.add(user)

    if image:
        user.image_url = image
        db.session.add(user)

    if no_image:
        user.image_url = 'https://www.sackettwaconia.com/wp-content/uploads/default-profile.png'
        db.session.add(user)

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    
    return redirect('/users')