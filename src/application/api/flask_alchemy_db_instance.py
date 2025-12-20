from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from src.adapters.sql.db_instance import DBInstance


class FlaskAlchemyDBInstance(DBInstance):

    def __init__(self, app: Flask):
        self.app = app
        self.sql_alchemy_instance = SQLAlchemy(self.app)

    def __get_sql_alchemy_instance(self) -> SQLAlchemy:
        return self.sql_alchemy_instance

    def get_db_engine(self) -> Engine:
        return self.__get_sql_alchemy_instance().engine

    def get_session(self) -> Session:
        return self.sql_alchemy_instance.session
