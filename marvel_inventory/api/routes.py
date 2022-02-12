from flask import Blueprint, jsonify, request
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, User, Character, character_schema, characters_schema
api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value'}

# create character route
@api.route('/characters', methods = ['POST'])
@token_required
def create_character(current_user_token):
    name = request.json['name']
    identity_name = request.json['identity_name']
    image_url = request.json['image_url']
    abilities = request.json['abilities']
    sub_universe = request.json['sub_universe']
    movie_appearances= request.json['movie_appearances']
    tv_appearances = request.json['tv_appearances']
    user_token = current_user_token.token


    character = Character(name, identity_name, image_url, abilities, sub_universe, movie_appearances, tv_appearances, user_token = user_token)

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

# Retrieve  all characters
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token = owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)

# Retrieve one character
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# update a character
@api.route('/characters/<id>', methods = ['POST','PUT'])
@token_required
def update_character(current_user_token,id):
    character = Character.query.get(id) # get character instance

    character.name = request.json['name']
    character.identity_name = request.json['identity_name']
    character.image_url = request.json['image_url']
    character.abilities = request.json['abilities']
    character.sub_universe = request.json['sub_universe']
    character.movie_appearances = request.json['movie_appearances']
    character.tv_appearances = request.json['tv_appearances']
    character.series = request.json['series']
    # character.user_token = current_user_token.token

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)

# delete a character
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)