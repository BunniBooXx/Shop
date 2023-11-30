from flask import Flask
from .models import db, User
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .shop import shop


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(shop)
CORS(app)

jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_caller(_jwt_header, jwt_data): 
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()




db.init_app(app)

migrate = Migrate(app,db)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

