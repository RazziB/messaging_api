from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from cerberus import Validator
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialization
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# Validators:
message_validator = Validator()
message_validator.schema = {
    "receiver": {'type': 'string', 'required': True, 'minlength':3, 'maxlength': 10},
    "message": {'type': 'string', 'required': True, 'minlength':3, 'maxlength':100},
    "subject": {'type': 'string', 'required': True, 'minlength':3, 'maxlength':20},
    "creation_date": {'type': 'string', 'required': False}
}

login_validator = Validator()
login_validator.schema = {
    "username": {'type': 'string', 'required': True, 'minlength': 3, 'maxlength': 10},
    "password": {'type': 'string', 'required': True, 'minlength': 3, 'maxlength': 10},
}

# Import here to avoid conflict
from messaging_api import routes
