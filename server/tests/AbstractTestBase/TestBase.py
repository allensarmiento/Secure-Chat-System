from unittest import TestCase
from ChatServer.Database import DatabaseManager
from ChatServer.Utilities import Singleton
from ChatServer.WebSocketServer import WebSocketServer
import sys


class TestBase(TestCase):
    def setUp(self) -> None:
        sys.argv = [sys.argv[0]]
        self.db = DatabaseManager.DatabaseManager(memory_db=True)
        self.ws = WebSocketServer.WebSocketServer()

    def tearDown(self) -> None:
        Singleton.Singleton.clear_instance_references()
        sys.argv = [sys.argv[0]]
