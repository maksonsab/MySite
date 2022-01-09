from os import environ


DEBUG = True
SECRET_KEY = environ['SECRET_KEY']
ENV = 'development'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

