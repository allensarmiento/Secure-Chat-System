from ChatServer.Database import DatabaseManager
from concurrent.futures import ThreadPoolExecutor
from ChatServer.WebSocketServer.EndPoints import Users
import asyncio


class WebSocketServer(object):
    def __init__(self):
        self.db = DatabaseManager.DatabaseManager()
        self.threadPool = ThreadPoolExecutor(10)
        asyncio.get_event_loop().set_default_executor(self.threadPool)
        self.users = Users.User()
        self.port = 1029
