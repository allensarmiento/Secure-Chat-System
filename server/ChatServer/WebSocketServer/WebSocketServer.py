from Database import DatabaseManager
from concurrent.futures import ThreadPoolExecutor
from WebSocketServer.EndPoints import Users
import asyncio
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import base64
from cryptography import fernet


class WebSocketServer(object):
    def __init__(self):
        self.db = DatabaseManager.DatabaseManager()
        self.threadPool = ThreadPoolExecutor(10)
        asyncio.get_event_loop().set_default_executor(self.threadPool)
        self.users = Users.User()
        self.port = 1029

    def get_app(self):
        app = web.Application()
        fernet_key = fernet.Fernet.generate_key()
        secret_key = base64.urlsafe_b64decode(fernet_key)
        setup(app, EncryptedCookieStorage(secret_key))
        app.router.add_post('/login', self.users.login)
        return app

    @classmethod
    def start_server(cls):
        server = cls()
        print("Started web server")
        web.run_app(server.get_app())
