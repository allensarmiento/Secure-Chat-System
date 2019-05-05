from WebSocketServer.EndPoints import EndPointBase
from aiohttp import web
from aiohttp.web import Request
from aiohttp_session import get_session
from Database.Tables import ChatUser


class User(EndPointBase.EndPointBase):
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
                if await self.run_executor(user.test_password, user_pass):
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
