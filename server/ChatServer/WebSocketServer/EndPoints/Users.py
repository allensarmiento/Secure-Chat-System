from WebSocketServer.EndPoints import EndPointBase
from aiohttp import web
from aiohttp.web import Request
from Database.Tables import ChatUser, ChatUserTokens
import traceback


class User(EndPointBase.EndPointBase):
    async def login(self, request: Request):
        try:
            body = await request.json()
            user_name = body.get('username')
            user_pass = body.get('password')
            if not user_name:
                return web.HTTPBadRequest(reason="You are missing the username field for the login user.")
            if not user_pass:
                return web.HTTPBadRequest(reason="You are missing the password field. Please send hashed password.")
            else:
                user: ChatUser.ChatUser = await ChatUser.ChatUser.get_user_byname(user_name)
                if not user:
                    return web.HTTPBadRequest(reason="This user is not registered with the system.")
                if await self.run_executor(user.test_password, user_pass):
                    data = {'id': user.get_id(), 'token': await ChatUser.ChatUser.generate_token(user.get_id())}
                    return web.json_response(data)
                else:
                    return web.HTTPForbidden(reason="Bad password.")
        except Exception as ex:
            traceback.print_exc()
            return web.HTTPServerError(text="{}".format(ex))

    async def user_name(self, request: Request):
        """returns the user's name"""
        try:
            user = await self.get_session_user(request)
            return web.json_response({'name': user.get_name()})
        except Exception as ex:
            traceback.print_exc()
            return web.HTTPInternalServerError(reason=str(ex))

    async def user_id(self, request: Request):
        try:
            user = await self.get_session_user(request)
            return web.json_response({'id': user.get_id()})
        except Exception as ex:
            traceback.print_exc()
            return web.HTTPInternalServerError(reason=str(ex))

    async def validate(self, request: Request):
        try:
            if await ChatUserTokens.ChatUserTokens.token_valid(await self.get_token(request)):
                return web.json_response({'valid': True})
            else:
                return web.json_response({'valid': False})
        except Exception as ex:
            traceback.print_exc()
            return web.HTTPInternalServerError(reason=str(ex))
