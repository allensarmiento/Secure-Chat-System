from unittest import TestCase
from Database import DatabaseManager
from Utilities import Singleton
from WebSocketServer import WebSocketServer
import sys


class TestBase(TestCase):
    def setUp(self) -> None:
        sys.argv = [sys.argv[0]]
        self.db = DatabaseManager.DatabaseManager(memory_db=True)
        self.ws = WebSocketServer.WebSocketServer()

    def tearDown(self) -> None:
        Singleton.Singleton.clear_instance_references()
        sys.argv = [sys.argv[0]]
