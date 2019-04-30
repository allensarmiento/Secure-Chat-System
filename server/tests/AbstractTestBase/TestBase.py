from unittest import TestCase
from ChatServer.Database import DatabaseManager
from ChatServer.Utilities import Singleton


class TestBase(TestCase):
    def setUp(self) -> None:
        self.db = DatabaseManager.DatabaseManager(memory_db=True)

    def tearDown(self) -> None:
        Singleton.Singleton.clear_instance_references()
