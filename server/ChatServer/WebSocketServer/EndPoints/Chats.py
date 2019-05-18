from WebSocketServer.EndPoints import EndPointBase
from aiohttp import web
from Database.Tables import ChatUser, ChatUserTokens, ChatSessions, ChatMessages
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

    async def send_message(self, request: Request):
        user = await self.get_session_user(request)
        channel_id = await self.get_field(request, "channel_id", str)
        message = await self.get_field(request, "message", str)
        signature = await self.get_field(request, "signature", str)
        resp = await ChatMessages.ChatMessages.send_message(channel_id, user.user_id, message, signature)
        return web.json_response(resp)

    async def get_messages(self, request: Request):
        user = await self.get_session_user(request)
        channel_id = await self.get_field(request, "channel_id", str)
        message_floor = await self.get_field(request, "message_floor", str)
        resp = await ChatMessages.ChatMessages.get_messages(channel_id, user.user_id, message_floor)
        return web.json_response({"messages" : resp})