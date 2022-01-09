from os import environ


from flask import Flask
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__, template_folder='templates')
app.config.update(
    DEBUG = True,
    SECRET_KEY = environ['SECRET_KEY'],
    ENV = 'development',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db',
    SQLALCHEMY_TRACK_MODIFICATIONS = False,

)

db = SQLAlchemy(app)

from app import routes