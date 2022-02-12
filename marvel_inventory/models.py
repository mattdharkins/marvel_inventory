# Standard
from distutils.log import Log
import uuid
from datetime import datetime
import secrets

# 3rd party imports
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(50), nullable = True, default='')
    last_name = db.Column(db.String(50), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref = 'owner', lazy = True)

    def __init__(self, first_name, last_name, email,  id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self,length):
        return secrets.token_hex(length)


    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Character(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(50))
    identity_name = db.Column(db.String(150), nullable = True)
    image_url = db.Column(db.String(500), nullable = True)
    abilities = db.Column(db.String(500), nullable = True)
    sub_universe = db.Column(db.String(100), nullable = True)
    movie_appearances = db.Column(db.String(500), nullable = True)
    tv_appearances = db.Column(db.String(500), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, identity_name, image_url, abilities, sub_universe, movie_appearances, tv_appearances, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.identity_name = identity_name
        self.image_url = image_url
        self.abilities = abilities
        self.sub_universe = sub_universe
        self.movie_appearances = movie_appearances
        self.tv_appearances = tv_appearances
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())

    def __repr__(self):
        return f'The following Character has been added: {self.name}'

# Creation of API Schema via the Marshmallow Object
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name','identity_name', 'image_url', 'image_url', 'abilities', 'sub_universe', 'movie_appearances', 'tv_appearances']

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)