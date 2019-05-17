from WebSocketServer.EndPoints import EndPointBase
from aiohttp import web
from Database.Tables import ChatUser, ChatUserTokens, ChatSessions
from aiohttp.web import Request


class Chats(EndPointBase.EndPointBase):
    async def start_chat_session(self, request: Request):
        user = await self.get_session_user(request)
        body = await request.json()
        users = body.get('usernames')
        if not isinstance(users, list):
            return web.HTTPBadRequest(reason="Provide a list of usernames to initiate a chat session with. ex usernames: ['user1', 'user2']")
        else:
            users.append(user.get_name())
            users = set(users)
            return web.json_response(await ChatSessions.ChatSessions.create_chat_session(users, user.get_id()))

    async def my_keys(self, request: Request):
        user = await self.get_session_user(request)
        return web.json_response(await ChatSessions.ChatSessions.get_my_sessions(user.get_id()))