from WebSocketServer.EndPoints import EndPointBase
from aiohttp import web
from aiohttp.web import Request
from Database.Tables import ChatUser, ChatUserTokens, ChatSessions
import traceback


class User(EndPointBase.EndPointBase):
    async def login(self, request: Request):
        #print("Line 10 in Users.py\n", await request.json())
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
                    await ChatUser.ChatUser.set_status(user.get_name(), "online")
                    return web.json_response(data)
                else:
                    return web.HTTPForbidden(reason="Bad password.")
        except Exception as ex:
            traceback.print_exc()
            return web.HTTPServerError(text="{}".format(ex))

    async def all_users(self, request: Request):
        user = await self.get_session_user(request)
        return web.json_response({"users" : await ChatUser.ChatUser.list_all_users(user.get_name())})

    async def user_name(self, request: Request):
        """returns the user's name"""
        user = await self.get_session_user(request)
        return web.json_response({'name': user.get_name()})

    async def user_id(self, request: Request):
        user = await self.get_session_user(request)
        return web.json_response({'id': user.get_id()})

    async def validate(self, request: Request):
        try:
            if await ChatUserTokens.ChatUserTokens.token_valid(await self.get_token(request)):
                return web.json_response({'valid': True})
            else:
                return web.json_response({'valid': False})
        except Exception as ex:
            traceback.print_exc()
            return web.HTTPInternalServerError(reason=str(ex))

    async def logout_single(self, request):
        try:
            await ChatUser.ChatUser.set_status((await self.get_session_user(request)).get_name(), "offline")
            await ChatUserTokens.ChatUserTokens.revoke_single_token(await self.get_token(request))
            return web.json_response({"deleted": True})
        except Exception as ex:
            return web.HTTPInternalServerError(reason=str(ex))

    async def logout_all(self, request):
        user = await self.get_session_user(request)
        try:
            await ChatUserTokens.ChatUserTokens.revoke_all_tokens(user.get_id())
            return web.json_response({"deleted": True})
        except Exception as ex:
            return web.HTTPInternalServerError(reason=str(ex))
    
    async def user_status(self, request: Request):
        """returns the user's status"""
        #print("user_status in Users.py\n", await request.json())
        body = await request.json()
        user = await ChatUser.ChatUser.get_user_byname(body.get('username'))
        return web.json_response({'name': body.get('username'), 'status': user.get_status()})

    async def user_publickey(self, request: Request):
        await self.get_session_user(request)
        requested_user = await self.get_field(request, "user_name", str)
        user = await ChatUser.ChatUser.get_user_byname(requested_user)
        if not user:
            raise web.HTTPNotFound(reason="User: {} not found.".format(requested_user))
        return web.json_response({'user_name': user.get_name(), 'public_key': await user.get_public_key()})
