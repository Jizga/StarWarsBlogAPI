from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey

#En este achivo se crean los modelos de las tablas de la BD

db = SQLAlchemy()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250))
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    favorite_characters = db.relationship('FavoriteCharacters', backref='User', lazy=True)

    favorite_planets = db.relationship('FavoritePlanets', backref='User', lazy=True)

    # tell python how to print the class object on the console
    def __repr__(self):
        return '<User %r>' % self.username

     # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email
            # do not serialize the password, its a security breach
        }


class Character(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(45))
    skin_color = db.Column(db.String(45))
    eye_color = db.Column(db.String(45))
    birth_year = db.Column(db.DateTime)
    gender  = db.Column(db.String(45))
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
    name  = db.Column(db.String(250))
    homeword = db.Column(db.String(250))
    url = db.Column(db.String(250))

    # tell python how to print the class object on the console
    def __repr__(self):
        return '<Character %r>' % self.name

    # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id": self.id,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "created": self.created,
            "edited": self.edited,
            "name": self.name,
            "homeword": self.homeword,
            "url": self.url
        }

class Planet(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
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

    # tell python how to print the class object on the console
    def __repr__(self):
        return '<Planet %r>' % self.name

    # tell python how convert the class object into a dictionary ready to jsonify
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

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)

    # tell python how to print the class object on the console
    #def __repr__(self):
        #return '<FavoriteCharacters %r>' % self.name

    # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class FavoritePlanets(db.Model):

    __tablename__ = 'favoritePlanets'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)


    # tell python how to print the class object on the console
    # def __repr__(self):
    #     return '<FavoritePlanets %r>' % self.name

    # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

