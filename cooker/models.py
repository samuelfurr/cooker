from cooker import db, login
from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import pdb

class User(UserMixin, db.Document):
    username = StringField(required=True, unique=True)
    password_hash = StringField()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.objects.get(pk=id)

class Card(db.Document):
    layout = StringField()    
    name = StringField()
    names = ListField()
    manaCost = StringField()
    cmc = IntField()
    colors = ListField()
    colorIdentity = ListField()
    type = StringField()
    supertypes = ListField()
    types = ListField()
    subtypes = ListField()
    rarity = StringField()
    text = StringField()
    flavor = StringField()
    artist = StringField()
    number = StringField()
    power = StringField()
    toughness = StringField()
    loyalty = IntField()
    multiverseid = IntField()
    variations = ListField()
    imageName = StringField()
    watermark = StringField()
    border = StringField()
    timeshifted = BooleanField()
    hand = IntField()
    life = IntField()
    reserved = BooleanField()
    releaseDate = StringField()
    starter = BooleanField()
    mciNumber = StringField()
    rulings = ListField()
    foreignNames = ListField()
    printings = ListField()
    originalText = StringField()
    originalType = StringField()    
    legalities = ListField()
    source = StringField()

    def __repr__(self):
        return '<Card {}>'.format(self.name)        
    
class Deck(db.Document):
    name = StringField(required=True)
    author = ReferenceField(User, required=True)
    description = StringField()
    artifacts = DictField()
    creatures = DictField()
    enchantments = DictField()
    instants = DictField()
    lands = DictField()
    sorceries = DictField()
    planeswalkers = DictField()
    
    side = ListField()
    
    meta = {'allow_inheritance' : True}

    def __repr__(self):
        return '<Deck {}>'.format(self.name)        

class Commander(Deck):
    commander = ReferenceField(Card)
    deck_size = 99
    legality = 'Commander'

class Vintage(Deck):
    deck_size = 60
    legality = 'Vintage'

class Legacy(Deck):
    deck_size = 60
    legality = 'Legacy'

class Modern(Deck):
    deck_size = 60
    legality = 'Modern'

    

