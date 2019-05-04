from ChatServer.Database import DatabaseManager
from concurrent.futures import ThreadPoolExecutor
from ChatServer.WebSocketServer.EndPoints import Users
import asyncio
from aiohttp import web
from aiohttp.web import Request
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import base64
from cryptography import fernet
from ChatServer.Database.Tables import ChatUser


class WebSocketServer(object):
    def __init__(self):
        self.db = DatabaseManager.DatabaseManager()
        self.threadPool = ThreadPoolExecutor(10)
        asyncio.get_event_loop().set_default_executor(self.threadPool)
        self.users = Users.User()
        self.port = 1029

    async def login(self, request: Request):
        session = await get_session(request)
        login_ok = False
        try:
            body = await request.json()
            user_id = session['id'] if 'id' in session else body.get('id')
            user_pass = body.get('password')
            if not user_id:
                return web.HTTPBadRequest(reason="You are missing the id field for the login user.")
            if not user_pass:
                return web.HTTPBadRequest(reason="You are missing the password field. Please send the password encrypted by your private key.")
            else:
                user: ChatUser.ChatUser = await ChatUser.ChatUser.get_user(user_id)
                if not user:
                    return web.HTTPBadRequest(reason="This user is not registered with the system.")
                if user.test_password(user_pass):
                    session['id'] = user_id
                    session['log_ok'] = True
                    login_ok = False
                    return web.Response(text="Login ok")
                else:
                    return web.HTTPForbidden(reason="Bad password.")
        except Exception as ex:
            print(ex)
            session.invalidate()
            return web.HTTPServerError(text="{}".format(ex))
        finally:
            if not login_ok:
                session.invalidate()

    def get_app(self):
        app = web.Application()
        fernet_key = fernet.Fernet.generate_key()
        secret_key = base64.urlsafe_b64decode(fernet_key)
        setup(app, EncryptedCookieStorage(secret_key))
        app.router.add_post('/login', self.login)
        return app

    @classmethod
    def start_server(cls):
        server = cls()
        print("Started web server")
        web.run_app(server.get_app())
