from Database import DatabaseManager
from concurrent.futures import ThreadPoolExecutor
from WebSocketServer.EndPoints import Users, Chats
import asyncio
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet
from Crypto.PublicKey import RSA
import base64
from Crypto.PublicKey.RSA import RsaKey


class WebSocketServer(object):
    def __init__(self):
        self.db = DatabaseManager.DatabaseManager()
        self.threadPool = ThreadPoolExecutor(10)
        asyncio.get_event_loop().set_default_executor(self.threadPool)
        self.users = Users.User()
        self.chats = Chats.Chats()
        self.private_key: RsaKey = None
        self.public_key: RsaKey = None
        self.load_key()

    def load_key(self):
        try:
            with open("server_private.pem") as f:
                self.private_key = RSA.import_key(f.read())
            with open("server_public.pem") as f:
                self.private_key = RSA.import_key(f.read())
        except:
            print("Server key pair does not exist. Creating new key pair now. This public key must be installed on all clients.")
            key = RSA.generate(4096)
            private = key.export_key("PEM")
            public = key.publickey().export_key("PEM")
            with open("server_private.pem", 'wb') as f:
                f.write(private)
            with open("server_public.pem", 'wb') as f:
                f.write(public)
            self.private_key = RSA.import_key(private)
            self.public_key = RSA.import_key(public)

    def get_app(self):
        app = web.Application()
        fernet_key = fernet.Fernet.generate_key()
        secret_key = base64.urlsafe_b64decode(fernet_key)
        setup(app, EncryptedCookieStorage(secret_key))
        app.router.add_post('/login', self.users.login)
        app.router.add_post('/users/name', self.users.user_name)
        app.router.add_post('/users/id', self.users.user_name)
        app.router.add_post('/users/status', self.users.user_status)
        app.router.add_post('/users/public_key', self.users.user_publickey)
        app.router.add_post('/users/all_users', self.users.all_users)
        app.router.add_post('/users/validate', self.users.validate)
        app.router.add_post('/chat/initiate', self.chats.start_chat_session)
        app.router.add_post('/chat/send', self.chats.send_message)
        app.router.add_post('/chat/messages', self.chats.get_messages)
        app.router.add_post('/chat/keys', self.chats.my_keys)
        app.router.add_delete('/users/logout', self.users.logout_single)
        app.router.add_delete('/users/logout_all', self.users.logout_all)
        return app

    @classmethod
    def start_server(cls):
        server = cls()
        print("Started web server")
        web.run_app(server.get_app())
