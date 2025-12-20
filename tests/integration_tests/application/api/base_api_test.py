from flask import Flask
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from injector import Injector
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from src.adapters.sql.db_instance import DBInstance
from src.application.api import register_controllers, DependencyInjector
from tests.integration_tests.base_db_integration_test import BaseDBIntegrationTest
from tests.mocks import FIRST_DEFAULT_ID, SECOND_DEFAULT_ID

SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
TESTING = True
ENCRYPT_SECRET_KEY = "tests"

app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = ENCRYPT_SECRET_KEY
app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"
app.config['JWT_AUTH_HEADER_PREFIX'] = "Bearer"

test_parameters = {
    "db_instance": None
}

class TestDBInstance(DBInstance):
    def __init__(self):
        self.sql_alchemy = None

    def __get_sql_alchemy_instance(self) -> SQLAlchemy:
        if not self.sql_alchemy:
            self.sql_alchemy = SQLAlchemy(app)
        return self.sql_alchemy

    def get_db_engine(self) -> Engine:
        return self.__get_sql_alchemy_instance().engine

    def get_session(self) -> Session:
        return self.sql_alchemy.session


class BaseAPITest(TestCase, BaseDBIntegrationTest):
    def create_app(self):
        return app

    def setUp(self):
        if not test_parameters["db_instance"]:
            self.db_instance = TestDBInstance()
            test_parameters["db_instance"] = self.db_instance
            self.db_engine = self.db_instance.get_db_engine()
            app_injector = Injector([DependencyInjector(app, self.db_instance)])
            register_controllers.instantiate_controllers(app, app_injector)

        self.db_instance = test_parameters["db_instance"]
        self.db_engine = self.db_instance.get_db_engine()

        self.token = f"Bearer {create_access_token(identity=str(FIRST_DEFAULT_ID))}"
        self.token_without_permission = f"Bearer {create_access_token(identity=str(SECOND_DEFAULT_ID))}"

        self._init_database()

    def tearDown(self):
        super().clear_database()

    def get_default_headers(self, with_permission: bool = True, with_token: bool = True) -> dict:
        token = self.token if with_permission else self.token_without_permission
        return {"Authorization": token if with_token else None}

    def get_db_engine(self) -> Engine:
        return self.db_instance.get_db_engine()
