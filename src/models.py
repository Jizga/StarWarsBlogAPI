from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    favorite_characters_fk = db.relationship('FavoriteCharacters', lazy=True)

    # tell python how to print the class object on the console
    def __repr__(self):
        return '<User %r>' % self.name

     # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "last_name": self.last_name,
            "favorite_characters_fk": list(map(lambda x: x.serialize(), self.favorite_characters_fk))
            # do not serialize the password, its a security breach
        }
        
class Characters(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(250))
    race = db.Column(db.String(250))
    age = db.Column(db.Integer)
    birth = db.Column(db.String(250))
    sex = db.Column(db.String(250))
    country = db.Column(db.String(250))
    favorite_characters_fk2 = db.relationship('FavoriteCharacters', lazy=True)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "race": self.race,
            "age": self.age,
            "birth": self.birth,
            "sex": self.sex,
            "country": self.country,
            "favorite_characters_fk2": list(map(lambda x: x.serialize(), self.favorite_characters_fk2))
        }

class Planets(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.Integer)
    rotation_planet = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.Integer)
    population = db.Column(db.Integer)
    climate = db.Column(db.String(45))
    terrain  = db.Column(db.String(45))
    surface_water = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    name  = db.Column(db.String(250))
    url = db.Column(db.String(250))
    #favorite_planets_id = db.Column(db.Integer, db.ForeignKey('favoritePlanets.id'))

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "diameter": self.diameter,
            "rotation_planet": self.rotation_planet,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created": self.created,
            "name": self.name,
            "url": self.url
        }

class FavoriteCharacters(db.Model):

    __tablename__ = 'favoriteCharacters'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    
    #character_id = db.relationship('Character', lazy=True)
    
    def __repr__(self):
        return '<FavoriteCharacters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            #"user_id": list(map(lambda x: x.serialize(), self.user_id))
        }

class FavoritePlanets(db.Model):

    __tablename__ = 'favoritePlanets'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    #user_id = db.relationship('User', lazy=True)
    #planet_id = db.relationship('Planets', lazy=True)

    def __repr__(self):
        return '<FavoritePlanets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            #"user_id": list(map(lambda x: x.serialize(), self.user_id))
        }

