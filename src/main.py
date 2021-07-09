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
from models import Character, Planet, FavoriteCharacters, FavoritePlanets

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
    
    # ---- Lo añade a la base de datos pero con los valores vacíos
    # json = request.get_json(force=True)
    # user = User(
    #         name = User.name ,
    #         last_name = User.last_name,
    #         email= User.email,
    #         password = User.password
    #         )
    
    # -------- Otra forma:
    body_request = request.get_json(force=True)
    print('?????? --- ', body_request) #---->>> Saca una lista con el/los usarios de Postman
    user = User(**body_request)
    db.session.add(user)
    db.session.commit()

    ## error -->> " TypeError: DefaultMeta object argument after ** must be a mapping, not list "
    return jsonify(user.serialize()), 201
   
    ## ---- INTENTO DE ARREGLO DEL ERROR DEL MAPPING:
    #body_request = request.get_json(force=True) #---->>> Saca una lista con el/los usarios de Postman
    
    # user = None
    # for req in body_request:
    #     user = User(**req)
    #     print('USUARIO ÚNICO AÑADIDO ---- ', user)
    # db.session.add(user)
    # db.session.commit()
    # ### error ---->>> "TypeError: Incompatible collection type: str is not list-like"
    # return jsonify(user.serialize()), 201




@app.route('/user/<int:id>', methods=[ 'GET'])
def get_single_user(id):
   
    # body = request.get_json() #{ 'username': 'new_username'}
    # #Modifica el nombre del usuario:
    # if request.method == 'PUT':
    #     user1 = User.query.get(id)
    #     user1.username = body.username
    #     db.session.commit()
   
    #     return jsonify(user1.serialize()), 200
         
    
    # if request.method == 'GET':
        user1 = User.query.get(id)
        
        return jsonify(user1.serialize()), 200

    #return "Invalid Method", 404

# @app.route('/character', methods=['GET'])
# def handle_hello():
#     response = jsonify(characters)
#     response.status_code = 200 
    
#     return response

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
