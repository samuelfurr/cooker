import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'testkey'

    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://cooker-jqcga.mongodb.net/test',
        'db': 'test',
        'username': 'sfurr',
        'password': 'CMJDdv3EYhDv7Biw',
        'connect': False
    }
