"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

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
    """Shows most recent posts"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('recent-posts.html', posts=posts)

# Routes for users

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
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')
    
# Routes for posts

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('post-form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_post(user_id):
    if not request.form['title'] or not request.form['content']:
        flash('Title and Content are required')
        return redirect(f'/users/{user_id}/posts/new')
    else:
        new_post = Post(title=request.form['title'], content=request.form['content'], user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('show-post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = request.form['title']
    content = request.form['content']

    if not title and not content:
        flash('No changes have been made.  Please make a change to either Title or Post Content')
        return redirect(f'/posts/{post_id}/edit')
    else:
        if title:
            post.title = title
            db.session.add(post)

        if content:
            post.content = content
            db.session.add(post)

        db.session.commit()

        return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

# Routes for tags
@app.route('/tags')
def show_all_tags():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tags-list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('show-tag.html', tag=tag)

@app.route('/tags/new')
def show_add_tag_form():
    return render_template('add-tag.html')

@app.route('/tags/new', methods=["POST"])
def add_new_tag():
    tag_name = request.form['name']

    if not tag_name:
        flash('Name field cannot be blank')
        return redirect('/tags/new')
    else:
        new_tag = Tag(name=tag_name)
        db.session.add(new_tag)
        db.session.commit()

        return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit-tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    new_tag_name = request.form['name']

    if not new_tag_name:
        flash('No changes made.  Make a change to tag name or click cancel')
        return redirect(f'/tags/{tag_id}/edit')
    else:
        tag.name = new_tag_name
        db.session.add(tag)
        db.session.commit()

        return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')