import asyncio
from Database.Tables import ChatUserTokens, ChatUser
from functools import partial
from aiohttp import web


class EndPointBase(object):
    @classmethod
    async def run_executor(cls, function_ptr, *args):
        return await asyncio.get_event_loop().run_in_executor(None, partial(function_ptr, *args))

    async def get_token(self, request):
        body = await request.json()
        token = body.get('token')
        if not token:
            raise web.HTTPBadRequest(reason="Missing token field.")
        else:
            return token

    async def get_session_user(self, request) -> ChatUser.ChatUser:
        """Loads the user database object or raises not authorized if user needs to login"""
        user = await ChatUserTokens.ChatUserTokens.get_user(await self.get_token(request))
        if not user:
            raise web.HTTPForbidden(reason="Expired or invalid token.")
        return user
