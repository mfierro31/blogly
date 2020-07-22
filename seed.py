"""Seed file to make sample data for users and posts db."""

from models import User, Post, Tag, PostTag, db
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
cher = User(first_name='Cher', image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Cher_in_2019_cropped.jpg/1200px-Cher_in_2019_cropped.jpg')
gaga = User(first_name='Lady', last_name='Gaga', image_url='https://i.insider.com/5c66ef2eeb3ce8278850c163?width=600&format=jpeg&auto=webp')

# Add posts
p1 = Post(title='Hey!', content='Whaazzzuuuuup!', user_id=1)
p2 = Post(title='My Drums', content='Are soooooo coooool, maaaaaaan!', user_id=1)
p3 = Post(title='When Can I Play Again?', content='Damn you, coronavirus!  Go away, so I can play again!', user_id=1)
p4 = Post(title='Thanos', content="Yeah, that's me.  I'm Thanos.", user_id=2)
p5 = Post(title='Ooooh-weee!', content="That's my catch phrase!  Ooooooh-weeee!", user_id=3)
p6 = Post(title='SNL Life', content='SNL has shut down.  I may be out of a job soon! Help!', user_id=4)
p7 = Post(title='I Miss My Little Monsters!', content='I wanna play for you all again sometime soon!', user_id=6)
p8 = Post(title='Do You Believe?', content='...IN LOVE, AFTER LOVE???', user_id=5)
p9 = Post(title='Piece of Toast Is A Piece of Shit', content='I hate that guy. Everyone hates that guy. He sucks. But Bobby and him have an especially bad relationship. They HATE each other!', user_id=4)
p10 = Post(title='My Favorite Roles', content='1. Thanos from Avengers, 2. Llewelyn Moss from No Country For Old Men, 3. Eddie Mannix from Hail Caesar!', user_id=2)
p11 = Post(title='Why Did Beth Shoot Me?', content='Ooooh-weeee, remember that??... how... how Beth shot me in that one episode?', user_id=3)
p12 = Post(title='Want Your Bad Romance!', content='I want your loving, I want your revenge, you and me could have a bad romance!', user_id=6)

# Add new objects to session, so they'll persist
db.session.add_all([lars, josh, poopy, gar, cher, gaga])
db.session.commit()

# Commit--otherwise, this never gets saved!
db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12])
db.session.commit()

# Add tags
tag1 = Tag(name='Fun')                                                                                                                                                                              

tag2 = Tag(name='Sad')                                                                                                                                                                            

tag3 = Tag(name='Crazy')                                                                                                                                                                            

tag4 = Tag(name='Funny')                                                                                                                                                                            

tag5 = Tag(name='Music')                                                                                                                                                                            

tag6 = Tag(name='Film/TV')

db.session.add_all([tag1, tag2, tag3, tag4, tag5, tag6])                                                                                                                                            

db.session.commit()

# Add posts/tags relationships
post_tag1 = PostTag(post_id=1, tag_id=1)                                                                                                                                                           

post_tag2 = PostTag(post_id=1, tag_id=3)                                                                                                                                                           

post_tag3 = PostTag(post_id=1, tag_id=4)

post_tag4 = PostTag(post_id=2, tag_id=4)                                                                                                                                                           

post_tag5 = PostTag(post_id=2, tag_id=5)                                                                                                                                                           

post_tag6 = PostTag(post_id=3, tag_id=2)                                                                                                                                                           

post_tag7 = PostTag(post_id=3, tag_id=5)                                                                                                                                                           

post_tag8 = PostTag(post_id=4, tag_id=4)                                                                                                                                                           

post_tag9 = PostTag(post_id=4, tag_id=6)                                                                                                                                                           

post_tag10 = PostTag(post_id=4, tag_id=3)                                                                                                                                                          

post_tag11 = PostTag(post_id=5, tag_id=4)                                                                                                                                                          

post_tag12 = PostTag(post_id=5, tag_id=6)                                                                                                                                                          

post_tag13 = PostTag(post_id=6, tag_id=2)                                                                                                                                                          

post_tag14 = PostTag(post_id=6, tag_id=3)                                                                                                                                                          

post_tag15 = PostTag(post_id=6, tag_id=6)

db.session.add_all([post_tag1, post_tag2, post_tag3, post_tag4, post_tag5, post_tag6, post_tag7, post_tag8, post_tag9, post_tag10, post_tag11, post_tag12, post_tag13, post_tag14, post_tag15])                                                                                                                                              

db.session.commit()