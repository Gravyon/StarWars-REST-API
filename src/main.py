"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# character = [
#     {"label": "My first task", "done": False}
# ]

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

###########################
# User GET queries
###########################

@app.route('/user', methods=['GET'])
def get_users():
    ###########################
    # Get all users
    ###########################
    users = User.query.all()
    print(users)
    results = list(map(lambda x: x.serialize(), users))
    return jsonify(results), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Get one user
    user = User.query.filter_by(id=user_id).first()
    print(user)
    results = user.serialize()
    return jsonify(results), 200

###########################
# Character GET queries
###########################

@app.route('/character', methods=['GET'])
def get_characters():
    ###########################
    # Get all characters
    ###########################
    characters = Character.query.all()
    print(characters)
    results = list(map(lambda x: x.serialize(), characters))
    return jsonify(results), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    ###########################
    # Get one character
    ###########################
    character = Character.query.filter_by(id=character_id).first()
    print(character)
    results = character.serialize()
    return jsonify(results), 200

###########################
# Planet GET queries
###########################

@app.route('/planet', methods=['GET'])
def get_planets():
    ###########################
    # Get all planets
    ###########################
    planets = Planet.query.all()
    print(planets)
    results = list(map(lambda x: x.serialize(), planets))
    print(results)
    return jsonify(results), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    ###########################
    # Get one planet
    ###########################
    planet = Planet.query.filter_by(id=planet_id).first()
    print(planet)
    results = planet.serialize()
    return jsonify(results), 200

###########################
# Favorites GET queries
###########################

@app.route('/favorites', methods=['GET'])
def get_favorites():
    ###########################
    # Get all favorites
    ###########################
    favorites = Favorites.query.all()
    print(favorites)
    results = list(map(lambda x: x.serialize(), favorites))
    print(results)
    return jsonify(results), 200

@app.route('/favorites/<int:favorites_id>', methods=['GET'])
def get_favorite(favorites_id):
    ###########################
    # Get one favorite
    ###########################
    favorites = Favorites.query.filter_by(id=favorites_id).first()
    print(favorites)
    results = favorites.serialize()
    return jsonify(results), 200

###########################
# User POST query
###########################

@app.route('/user', methods=['POST'])
def create_user():
    # Load data from postman or input
    body = json.loads(request.data)
    print(body)
    # Filter by to check input email, this will be used in the if so email is never repeated
    user_query = User.query.filter_by(email=body["email"]).first()
    print(user_query)
    
    # If to check if user doesn't exist (by checking the email), if so, it's created
    if user_query is None:
        # Table contents, same as the one in models.py
        new_user = User(
        username=body["username"],
        name=body["name"],
        lastname=body["lastname"],
        password=body["password"],
        email=body["email"])
        print(new_user)
        # Flask command to add a new entry
        db.session.add(new_user)
        # Flask command to commit the database, saving the changes
        db.session.commit()
        # Standard response to request with error code 200 (success)
        response_body = {
            "msg": "New user created"
        }
        return jsonify(response_body), 200
    # else response if the email exists
    response_body = {
        "msg": "User email already exists"
    }
    # Ends the function by sending the error code 400 (data already exists)
    return jsonify(response_body), 400

###########################
# Planet POST query
###########################

@app.route('/planet', methods=['POST'])
def create_planet():
    # Load data from postman or input
    body = json.loads(request.data)
    print(body)
    # Filter by to check input name, this will be used in the if so name is never repeated
    planet_query = Planet.query.filter_by(name=body["name"]).first()
    print(planet_query)
    
    # "If" to check if planet doesn't exist (by checking the name), if so, it's created
    if planet_query is None:
        # Table contents, same as the one in models.py
        new_planet = Planet(name=body["name"])
        # Flask command to add a new entry
        db.session.add(new_planet)
        # Flask command to commit the database, saving the changes
        db.session.commit()
        # Standard response to request with error code 200 (success)
        response_body = {
            "msg": "New planet created"
        }
        return jsonify(response_body), 200
    # else response if the name exists
    response_body = {
        "msg": "Planet already exists"
    }
    # Ends the function by sending the error code 400 (data already exists)
    return jsonify(response_body), 400

###########################
# Character POST query
###########################


@app.route('/character', methods=['POST'])
def create_character():
    # Load data from postman or input
    body = json.loads(request.data)
    print(body)
    # Filter by to check input name, this will be used in the if so name is never repeated
    character_query = Character.query.filter_by(name=body["name"]).first()
    print(character_query)
    
    # "If" to check if character doesn't exist (by checking the name), if so, it's created
    if character_query is None:
        # Table contents, same as the one in models.py
        new_character = Character(name=body["name"])
        # Flask command to add a new entry
        db.session.add(new_character)
        # Flask command to commit the database, saving the changes
        db.session.commit()
        # Standard response to request with error code 200 (success)
        response_body = {
            "msg": "New character created"
        }
        return jsonify(response_body), 200
    # else response if the name exists
    response_body = {
        "msg": "character already exists"
    }
    # Ends the function by sending the error code 400 (data already exists)
    return jsonify(response_body), 400


################################
# Favorite character POST query
###############################

@app.route('/favorites/character/<int:user_id>/<int:char_id>', methods=['POST'])
def create_favorite_character(user_id, char_id):

    fav_user_char = Favorites.query.filter_by(user_id=user_id).first()
    fav_char_id = Favorites.query.filter_by(id_character=char_id).first()

    if fav_user_char and fav_char_id:
        response_body = {
            "msg": "This character exists in that user favorites list"
        }
        return jsonify(response_body), 400
    else :
        new_planet_fav = Favorites(user_id=user_id, id_character=char_id)
        db.session.add(new_planet_fav)
        db.session.commit()
        response_body = {
        "msg": "New character added to user list"
    }
    # Ends the function by sending the error code 400 (data already exists)
    return jsonify(response_body), 200


    response_body = {
        "msg": "character already exists"
    }
    # Ends the function by sending the error code 400 (data already exists)
    return jsonify(response_body), 400


# ###########################
# # Favorite planet POST query
# ###########################

@app.route('/favorites/planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def create_favorite_planet(user_id, planet_id):

    fav_user_planet = Favorites.query.filter_by(user_id=user_id).first()
    fav_planet_id = Favorites.query.filter_by(id_planet=planet_id).first()

    if fav_user_planet and fav_planet_id:
        response_body = {
            "msg": "This planet exists in that user favorites list"
        }
        return jsonify(response_body), 400
    else :
        new_planet_fav = Favorites(user_id=user_id, id_planet=planet_id)
        db.session.add(new_planet_fav)
        db.session.commit()
        response_body = {
        "msg": "New planet added to user list"
    }
    # Ends the function by sending the error code 400 (data already exists)
    return jsonify(response_body), 200


    response_body = {
        "msg": "planet already exists"
    }
    # Ends the function by sending the error code 400 (data already exists)
    return jsonify(response_body), 400


# ###########################
# NO FUNCIONA, NO SE PIDE
# # Favorites POST query
# ###########################
# @app.route('/favorites', methods=['POST'])
# def create_favorites():
#     # Load data from postman or input
#     body = json.loads(request.data)
#     print(body)

#     user_query = User.query.filter_by(id=body["user_id"]).first()
#     planet_query = Planet.query.filter_by(id=body["id_planet"]).first()
#     character_query = Character.query.filter_by(id=body["id_character"]).first()

#     print(user_query)
#     print(planet_query)
#     print(character_query)
    
#     if user_query:
#         response_body = {
#             "msg": "User exists"
#         }

#     elif user_query is None:
#         new_favorites = Favorites(
#         user_id=body["user_id"],
#         id_planet=body["id_planet"],
#         id_character=body["id_character"])
#         # Flask command to add a new entry
#         db.session.add(new_favorites)
#         # Flask command to commit the database, saving the changes
#         db.session.commit()
#         # Standard response to request with error code 200 (success)
#         response_body = {
#             "msg": "New favorite list created"
#         }
#         return jsonify(response_body), 200

#     # elif user_query and not planet_query or not character_query:
#     #     response_body = {
#     #         "msg": "Planet or character doesn't exist"
#     #     }
#     #     return jsonify(response_body), 400

#     response_body = {
#         "msg": "Error"
#     }
#     # Ends the function by sending the error code 400 (data already exists)
#     return jsonify(response_body), 400
    

###########################
# User DELETE query
###########################

@app.route('/user/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):

    user = User.query.filter_by(id=user_id).first()
    print(user)
    # If user exists, deletes it
    if user:
        db.session.delete(user)
        db.session.commit()
        response_body = {
            "msg": "User deleted successfully"
            }
        return jsonify(response_body), 200

    elif user is None:
        raise APIException('User not found', status_code=404)
        return jsonify(user)


###########################
# Planet DELETE query
###########################

@app.route('/planet/<int:planet_id>', methods=["DELETE"])
def delete_planet(planet_id):

    planet = Planet.query.filter_by(id=planet_id).first()
    print(planet)

    if planet:
        db.session.delete(planet)
        db.session.commit()
        response_body = {
            "msg": "Planet deleted successfully"
            }
        return jsonify(response_body), 200

    elif planet is None:
        raise APIException('Planet not found', status_code=404)
        return jsonify(planet)


###########################
# Character DELETE query
###########################

@app.route('/character/<int:character_id>', methods=["DELETE"])
def delete_character(character_id):

    character = Character.query.filter_by(id=character_id).first()
    print(character)

    if character:
        db.session.delete(character)
        db.session.commit()
        response_body = {
            "msg": "character deleted successfully"
            }
        return jsonify(response_body), 200

    elif character is None:
        raise APIException('character not found', status_code=404)
        return jsonify(character)


###########################
# Favorite DELETE all query
###########################

@app.route('/favorites/<int:favorite_id>', methods=["DELETE"])
def delete_favorite(favorite_id):

    favorite = Favorites.query.filter_by(id=favorite_id).first()
    # print(jsonify(favorite))

    if favorite is None:
        response_body = {
            "msg": "Favorite not found"
            }
        return jsonify(response_body), 404


    db.session.delete(favorite)
    db.session.commit()
    response_body = {
        "msg": "Favorite deleted successfully"
        }
    return jsonify(response_body), 200


# ###########################
# # Favorite planet DELETE query
# ###########################

@app.route('/favorites/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):

    fav_user_planet = Favorites.query.filter_by(user_id=user_id).first()
    fav_planet_id = Favorites.query.filter_by(id_planet=planet_id).first()

    if fav_user_planet is None and fav_planet_id is None:
        response_body = {
            "msg": "Planet or user not found"
        }
        return jsonify(response_body), 400
    else :
        planet_fav = Favorites.query.filter_by(user_id=user_id).filter_by(id_planet=planet_id).first()
        db.session.delete(planet_fav)
        db.session.commit()
        response_body = {
        "msg": "Planet deleted from user list"
    }
    # Ends the function by sending the error code 400 (data already exists)
    return jsonify(response_body), 200


    response_body = {
        "msg": "Error"
    }
    # Ends the function by sending the error code 400 (data already exists)
    return jsonify(response_body), 400


 # ###########################
# # Favorite character DELETE query
# ###########################

@app.route('/favorites/character/<int:user_id>/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):

    fav_user_character = Favorites.query.filter_by(user_id=user_id).first()
    fav_character_id = Favorites.query.filter_by(id_character=character_id).first()

    if fav_user_character is None and fav_character_id is None:
        response_body = {
            "msg": "character or user not found"
        }
        return jsonify(response_body), 400
    else :
        character_fav = Favorites.query.filter_by(user_id=user_id).filter_by(id_character=character_id).first()
        db.session.delete(character_fav)
        db.session.commit()
        response_body = {
        "msg": "character deleted from user list"
    }
    # Ends the function by sending the error code 400 (data already exists)
    return jsonify(response_body), 200


    response_body = {
        "msg": "Error"
    }
    # Ends the function by sending the error code 400 (data already exists)
    return jsonify(response_body), 400


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
