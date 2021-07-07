"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
##Aquí se realiza la unión con la BD
import os
from flask import Flask, request, jsonify, url_for
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


# characters = [
#     { 
#      "id": "1", 
#      "height": "170", 
#      "mass": "70",
#      "hair_color": "red",
#      "skin_color": "white", 
#      "eye_color": "red",
#      "birth_year": "1988-02-01",
#      "gender": "male",
#      "created": "1988-02-01",
#      "edited": "",
#      "name": "Nol",
#      "homeword": "",
#      "url": ""
#      },
#     { 
#      "id": "2", 
#      "height": "160", 
#      "mass": "60",
#      "hair_color": "red",
#      "skin_color": "white", 
#      "eye_color": "red",
#      "birth_year": "1996-04-07",
#      "gender": "female",
#      "created": "1988-02-01",
#      "edited": "",
#      "name": "Eliff",
#      "homeword": "",
#      "url": ""
#      }
# ]

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
    #Unión con la tabla "User" de la BD
    response = db.session.query(User).all()
    return jsonify(response), 200

@app.route('/user', methods=['POST'])
def add_new_user():
    
    json = request.get_json(force=True)

    if json.get('username') is None:
        return jsonify({'message': 'Bad request'}), 400

    user = User.create(json['username'])

    return jsonify({'user': user.json() })
    
   # response = {'message': 'success'}
    #return jsonify(response)




@app.route('/user/<int:user_id>', methods=['PUT', 'GET'])
def get_single_user(user_id):
   
    body = request.get_json() #{ 'username': 'new_username'}
    #Modifica el nombre del usuario:
    if request.method == 'PUT':
        user1 = User.query.get(user_id)
        user1.username = body.username
        db.session.commit()
   
        return jsonify(user1.serialize()), 200
         
    
    if request.method == 'GET':
        user1 = User.query.get(user_id)
        
        return jsonify(user1.serialize()), 200

    return "Invalid Method", 404

# @app.route('/character', methods=['GET'])
# def handle_hello():
#     response = jsonify(characters)
#     response.status_code = 200 
    
#     return response

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
