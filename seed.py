"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
mike = User(first_name='Mike', last_name='Fierro')
josh = User(first_name='Josh', last_name='Brolin')
gar = User(first_name='Garrmanaarnaar', last_name='Glooch', image_url='https://vignette.wikia.nocookie.net/rickandmorty/images/4/41/Garmanarnar.PNG/revision/latest/top-crop/width/360/height/450?cb=20160117000927')
gaga = User(first_name='Lady', last_name='Gaga', image_url='https://i.insider.com/5c66ef2eeb3ce8278850c163?width=600&format=jpeg&auto=webp')

# Add new objects to session, so they'll persist
db.session.add(mike)
db.session.add(josh)
db.session.add(gar)
db.session.add(gaga)

# Commit--otherwise, this never gets saved!
db.session.commit()