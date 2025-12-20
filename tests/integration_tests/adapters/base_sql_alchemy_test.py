from unittest import TestCase

from flask import Flask
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker

from src.adapters.sql.db_instance import DBInstance
from tests.integration_tests.base_db_integration_test import BaseDBIntegrationTest

test_app = Flask(__name__)


class TestDBInstance(DBInstance):

    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def get_db_engine(self) -> Engine:
        return self.db_engine

    def get_session(self) -> Session:
        return sessionmaker(autocommit=False, autoflush=False, bind=self.db_engine)()



class BaseSQLAlchemyTest(TestCase, BaseDBIntegrationTest):

    def setUp(self):
        self.db_engine = create_engine("sqlite:///:memory:")
        self.db_instance = TestDBInstance(self.db_engine)

        self._init_database()

    def tearDown(self):
        super().clear_database()

    def get_db_engine(self) -> Engine:
        return self.db_engine
