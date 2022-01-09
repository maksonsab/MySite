from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import app.config as Config




app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes