from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_login import UserMixin

connect('ChessDB')

class User(UserMixin,DynamicDocument):
    username = StringField(required=True)
    password = StringField(required=True)
    email = EmailField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    totalPoints = IntField(default=0) 
    totalWins = IntField(default=0)
    def set_password(self,password):
        self.password = generate_password_hash(password)

    def get_password(self,password):
        return check_password_hash(self.password,password)

class Game(DynamicDocument):
    whitePlayer = ReferenceField(User,reverse_delete_rule=NULLIFY)
    blackPlayer = ReferenceField(User,reverse_delete_rule=NULLIFY)
    room = StringField(required=True)
    pgn = StringField()
    fen = StringField()
    winner = ReferenceField(User,reverse_delete_rule=NULLIFY)
    created_at = DateTimeField(default=datetime.datetime.now)