"""Seed file to make sample data for pets db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
lars = User(first_name='Lars', last_name='Ulrich', image_url='https://metalheadzone.com/wp-content/uploads/2019/05/lars-ulrich-2019.jpg')
josh = User(first_name='Josh', last_name='Brolin', image_url='https://pmcvariety.files.wordpress.com/2019/02/josh-brolin.jpg?w=681&h=383&crop=1')
poopy = User(first_name='Poopy', last_name='Butthole', image_url='https://www.pngitem.com/pimgs/m/122-1228795_mr-poopybutthole-rick-and-morty-png-download-bill.png')
gar = User(first_name='Garrmanaarnaar', image_url='https://vignette.wikia.nocookie.net/rickandmorty/images/4/41/Garmanarnar.PNG/revision/latest/top-crop/width/360/height/450?cb=20160117000927')
cher = User(first_name='Cher')
gaga = User(first_name='Lady', last_name='Gaga', image_url='https://i.insider.com/5c66ef2eeb3ce8278850c163?width=600&format=jpeg&auto=webp')

# Add posts
p1 = Post(title='Hey!', content='Whaazzzuuuuup!', user_id=1)
p2 = Post(title='My Drums', content='Are soooooo coooool, maaaaaaan!', user_id=1)
p3 = Post(title='When Can I Play Again?', content='Damn you, coronavirus!  Go away, so I can play again!', user_id=1)
p4 = Post(title='Thanos', content="Yeah, that's me.  I'm Thanos.", user_id=2)
p5 = Post(title='Ooooh-weee!', content="That's my catch phrase!  Ooooooh-weeee!", user_id=3)
p6 = Post(title='SNL Life', content='SNL has shut down.  I may be out of a job soon! Help!', user_id=4)
p7 = Post(title='I Miss My Little Monsters!', content='I wanna play for you all again sometime soon!', user_id=6)

# Add new objects to session, so they'll persist
db.session.add_all([lars, josh, poopy, gar, cher, gaga])
db.session.commit()

# Commit--otherwise, this never gets saved!
db.session.add_all([p1, p2, p3, p4, p5, p6, p7])
db.session.commit()