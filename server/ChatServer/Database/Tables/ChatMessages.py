from Database.Tables import DeclarativeBase, ChatUser, ChatSessionUsers
from sqlalchemy import Column, Integer, LargeBinary, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
import datetime
import asyncio
from functools import partial
from Database import DatabaseManager
from aiohttp import web


class ChatMessages(DeclarativeBase.Base):
    __tablename__ = 'chatmessages'

    message_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    chat_session_id = Column(Integer, ForeignKey("chatsessions.channel_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("chatusers.user_id"), nullable=False)
    message = Column(LargeBinary, nullable=False)  # key encrypted using user's public key and base 64 encoded
    timestamp = Column(DateTime, nullable=False)
    signature_method = Column(String, default="AES", nullable=False)

    object_chat_session = relationship("ChatSessions", uselist=False, back_populates="object_session_messages")
    object_user = relationship("ChatUser", uselist=False, back_populates="object_user_sent_messages")


    def __init__(self, object_chat_session: ChatSessionUsers.ChatSessionUsers, message, signature):
        self.chat_session_id = object_chat_session.chat_session_id
        self.user_id = object_chat_session.user_id
        self.timestamp = datetime.datetime.utcnow()
        self.message = message.encode()
        self.signature_method = signature

    def json_message(self):
        return {"message_id": self.message_id,
                "time": str(self.timestamp),
                "user_id" : self.object_user.get_id(),
                "user_name" : self.object_user.get_name(),
                "signature" : self.signature_method,
                "message": self.message.decode()
        }

    @classmethod
    def _get_messages(cls, channel_id, user_id, msg_id):
        db = DatabaseManager.DatabaseManager.get_session()
        try:
            session = db.query(ChatSessionUsers.ChatSessionUsers).filter(
                ChatSessionUsers.ChatSessionUsers.chat_session_id == channel_id,
                ChatSessionUsers.ChatSessionUsers.user_id == user_id).one_or_none()
            if not session:
                raise web.HTTPUnauthorized(reason="User does not have access to this chat.")
            else:
                messages = []
                for m in db.query(cls).filter(cls.message_id > msg_id, cls.chat_session_id == channel_id).all():
                    messages.append(m.json_message())
                return messages
        finally:
            db.close()

    @classmethod
    def _send_message(cls, channel_id, user_id, msg, signature):
        db = DatabaseManager.DatabaseManager.get_session()
        try:
            session = db.query(ChatSessionUsers.ChatSessionUsers).filter(
                ChatSessionUsers.ChatSessionUsers.chat_session_id == channel_id,
                ChatSessionUsers.ChatSessionUsers.user_id == user_id).one_or_none()
            if not session:
                raise web.HTTPUnauthorized(reason="User does not have access to this chat.")
            if signature != "AES" and signature != "DES":
                raise web.HTTPBadRequest(reason="Signature must be either AES or DES.")
            else:
                db.add(cls(session, msg, signature))
                db.commit()
                top_message = db.query(cls).filter(cls.chat_session_id == channel_id).order_by(cls.message_id.desc()).first()
                if top_message:
                    return {"top_message_id" : top_message.message_id}
                else:
                    return {"top_message_id": -1}
        finally:
            db.close()

    @classmethod
    async def send_message(cls, channel_id, user_id, msg, signature):
        return await asyncio.get_event_loop().run_in_executor(None, partial(cls._send_message, channel_id, user_id, msg, signature))

    @classmethod
    async def get_messages(cls, channel_id, user_id, msg_floor):
        return await asyncio.get_event_loop().run_in_executor(None, partial(cls._get_messages, channel_id, user_id, msg_floor))

