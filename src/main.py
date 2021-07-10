"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
##Aquí se realiza la unión con la BD
import os
from flask import Flask, request, jsonify, url_for
import json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import Planets, Characters, FavoriteCharacters, FavoritePlanets

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    
    #.filter_by(deleted_at=None) --->>> siginifica que coge aquellos que no estén borrados
    
    list_obj = []
    
    #Unión con la tabla "User" de la BD
    response_list = User.query.all() ## ---->> Esto da una lista de usarios y se quiere un solo usario para ser serializado
    
    for obj in response_list:
        list_obj.append(obj.serialize())
    
    return jsonify(list_obj), 200

@app.route('/users', methods=['POST'])
def add_new_user():
    #Datos procedentes del body del POST de Postman
    body_request = request.get_json()
    
    #Unión con las columnas de la BD, los datos son del body de Postman
    name_request = body_request.get("name", None)
    last_name_request = body_request.get("last_name", None)
    email_request = body_request.get("email", None)
    password_request = body_request.get("password", None)
    
    new_user = User(
        name = name_request,
        email = email_request,
        last_name = last_name_request,
        password = password_request,
    )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@app.route('/people', methods=['POST'])
def add_new_character():

    body_request = request.get_json()
    
    name_request = body_request.get("name", None)
    race_request = body_request.get("race", None)
    age_request = body_request.get("age", None)
    birth_request = body_request.get("birth", None)
    sex_request = body_request.get("sex", None)
    country_request = body_request.get("country", None)
    
    new_character = Characters(
        name = name_request,
        race = race_request,
        age = age_request,
        birth = birth_request,
        sex = sex_request,
        country = country_request
    )
    
    db.session.add(new_character)
    db.session.commit()

    return jsonify(new_character.serialize()), 201


@app.route('/people', methods=['GET'])
def get_characters():
        
    characters_list = []
    response_list = Characters.query.all()
    
    for character in response_list:
        characters_list.append(character.serialize())
    
    return jsonify(characters_list), 200


@app.route('/planets', methods=['POST'])
def add_new_planet():

    body_request = request.get_json()
    
    name_request = body_request.get("name", None)
    diameter_request = body_request.get("diameter", None)
    rotation_planet_request = body_request.get("rotationPlanet", None)
    orbital_period_request = body_request.get("orbitalPeriod", None)
    gravity_request = body_request.get("gravity", None)
    population_request = body_request.get("population", None)
    
    new_planet = Planets(
        name = name_request,
        diameter = diameter_request,
        rotation_planet = rotation_planet_request,
        orbital_period = orbital_period_request,
        gravity = gravity_request,
        population = population_request
    )
    
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 201

@app.route('/planets', methods=['GET'])
def get_planets():
        
    planets_list = []
    response_list = Planets.query.all()
    
    for planet in response_list:
        planets_list.append(planet.serialize())
    
    return jsonify(planets_list), 200

@app.route('/people/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    body = request.get_json()
    character_selected = Characters.query.get(character_id)
    return jsonify(character_selected.serialize()), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    body = request.get_json()
    planet_selected = Planets.query.get(planet_id)
    return jsonify(planet_selected.serialize()), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    body = request.get_json()
    user_selected = User.query.get(user_id)
    return jsonify(user_selected.serialize()), 200
    
@app.route('/favorite/people', methods = ['POST', 'DELETE'])
def favorite_characters_list():
    
    body_request = request.get_json()
    
    if request.method == 'POST':
        user_id_request = body_request.get("user_id", None)
        character_id_request = body_request.get("character_id", None)
        
        favourite_list = FavoriteCharacters(
            user_id = user_id_request,
            character_id = character_id_request
        )
        
        db.session.add(favourite_list)
        db.session.commit()

        return jsonify(favourite_list.serialize()), 201
    
    if request.method == 'DELETE':
        # Datos necesarios para encontrar la lista de fovaritos para borrar
        user_id_request = body_request.get("user_id", None)
        character_id_request = body_request.get("character_id", None)
        
        # Lista encontrada, saca la primera coincidencia
        favourite_list_to_delete = FavoriteCharacters.query.filter_by(user_id = user_id_request, character_id = character_id_request).first_or_404()

        try:
            db.session.delete(favourite_list_to_delete)
            db.session.commit()
            return jsonify({"msg":"Deleted successfully"}), 200
            
        except:
            return "There was a problem deleting this character...", 400
        

@app.route('/favorite/planet', methods = ['POST', 'DELETE'])
def favorite_planets_list():
    body_request = request.get_json()
    favourite_list = []
    
    if request.method == 'POST':
        user_id_request = body_request.get("user_id", None)
        planet_id_request = body_request.get("planet_id", None)
        
        favourite_list = FavoritePlanets(
            user_id = user_id_request,
            planet_id = planet_id_request
        )

        db.session.add(favourite_list)
        db.session.commit()
        return jsonify(favourite_list.serialize()), 201
    
    if request.method == 'DELETE':
        user_id_request = body_request.get("user_id", None)
        planet_id_request = body_request.get("planet_id", None)
        
        favourite_list_to_delete = FavoritePlanets.query.filter_by(user_id = user_id_request, planet_id = planet_id_request).first_or_404()

        try:
            db.session.delete(favourite_list_to_delete)
            db.session.commit()
            return jsonify({"msg":"Deleted successfully"}), 200
            
        except:
            return "There was a problem deleting this character...", 400
        
        
@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_user_favourites(user_id):
    body = request.get_json()
    user_selected = User.query.get(user_id)
    favourite_list = user_selected["favorite_characters_fk"].append(user_selected["favorite_planets_fk"])
    
    return jsonify(favourite_list.serialize()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
