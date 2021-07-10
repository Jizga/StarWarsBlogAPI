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

@app.route('/user', methods=['GET'])
def handle_hello():
    
    #.filter_by(deleted_at=None) --->>> siginifica que coge aquellos que no estén borrados
    
    list_obj = []
    
    #Unión con la tabla "User" de la BD
    response_list = User.query.all() ## ---->> Esto da una lista de usarios y se quiere un solo usario para ser serializado
    
    for obj in response_list:
        list_obj.append(obj.serialize())
    
    return jsonify(list_obj), 200

@app.route('/user', methods=['POST'])
def add_new_user():
    #Datos procedentes del body del POST de Postman
    body_request = request.get_json()
    
    #Unión con las columnas de la BD, los datos son del body de Postman
    name_request = body_request.get("name", None)
    last_name_request = body_request.get("last_name", None)
    email_request = body_request.get("email", None)
    password_request = body_request.get("password", None)
    
    user = User(
        name = name_request,
        email = email_request,
        last_name = last_name_request,
        password = password_request,
    )
    
    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize()), 201

@app.route('/people', methods=['POST'])
def add_new_character():
    #Datos procedentes del body del POST de Postman
    body_request = request.get_json()
    
    #Unión con las columnas de la BD, los datos son del body de Postman
    name_request = body_request.get("name", None)
    race_request = body_request.get("race", None)
    age_request = body_request.get("age", None)
    birth_request = body_request.get("birth", None)
    sex_request = body_request.get("sex", None)
    country_request = body_request.get("country", None)
    
    character = Characters(
        name = name_request,
        race = race_request,
        age = age_request,
        birth = birth_request,
        sex = sex_request,
        country = country_request
    )
    
    db.session.add(character)
    db.session.commit()

    return jsonify(character.serialize()), 201



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
