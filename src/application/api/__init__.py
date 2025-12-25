from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from injector import Injector

from src import config
from src.application.api.dependency_injector import DependencyInjector
from src.application.api.flask_alchemy_db_instance import FlaskAlchemyDBInstance
from src.application.api.register_controllers import instantiate_controllers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.API_TOKEN_SECRET
app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=config.API_TOKEN_EXPIRATION_HOURS)
app.config['JWT_AUTH_HEADER_PREFIX'] = "Bearer"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_size": 10,          # number of connections to keep open
    "max_overflow": 20,       # allowed overflow connections
    "pool_timeout": 30,       # seconds to wait before giving up
    "pool_recycle": 300,     # refresh connections every 30 min
}

if config.ADD_ALLOW_CORS:
    CORS(app)

db_instance = FlaskAlchemyDBInstance(app)
app_injector = Injector([DependencyInjector(app, db_instance)])

instantiate_controllers(app, app_injector)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
