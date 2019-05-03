from ChatServer.Database import DatabaseManager
from concurrent.futures import ThreadPoolExecutor
from ChatServer.WebSocketServer.EndPoints import Users
import asyncio
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage


class WebSocketServer(object):
    def __init__(self):
        self.db = DatabaseManager.DatabaseManager()
        self.threadPool = ThreadPoolExecutor(10)
        asyncio.get_event_loop().set_default_executor(self.threadPool)
        self.users = Users.User()
        self.port = 1029

    async def login(self, request):
        return web.Response(text="Hello, world")

    def get_app(self):
        app = web.Application()
        app.add_routes([web.get('/login', self.login)])
        return app

    @classmethod
    def start_server(cls):
        server = cls()
        print("Started web server")
        web.run_app(server.get_app())
