from Database.Tables import DeclarativeBase, ChatUser, ChatSessionUsers
from sqlalchemy import Column, Integer, String, LargeBinary, Binary, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import asyncio
from functools import partial
import secrets
from Database import DatabaseManager
from aiohttp import web
import traceback
from sqlalchemy.orm.exc import NoResultFound


class ChatSessions(DeclarativeBase.Base):
    __tablename__ = 'chatsessions'

    channel_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    object_session_users = relationship("ChatSessionUsers", cascade="save-update,merge,delete,delete-orphan",
                                      uselist=True,
                                      back_populates="object_chat_session")

    def __init__(self):
        return

    @classmethod
    def _get_my_sessions(cls, user_id):
        db = DatabaseManager.DatabaseManager.get_session()
        try:
            response = []
            for csession in db.query(ChatSessionUsers.ChatSessionUsers).filter(ChatSessionUsers.ChatSessionUsers.user_id == user_id).all():
                response.append({"chat_session_id" : csession.chat_session_id, "symmetric_key" : csession.get_key()})
            return response
        finally:
            db.close()

    @classmethod
    def _create_chat_session(cls, user_names):
        db = DatabaseManager.DatabaseManager.get_session()
        try:
            session = cls()
            db.add(session)
            db.commit()
            key = secrets.token_urlsafe(128)
            for user in db.query(ChatUser.ChatUser).all():
                if user.get_name() in user_names:
                    db.add(ChatSessionUsers.ChatSessionUsers(session, user, key))
            db.commit()
        finally:
            db.close()

    @classmethod
    async def create_chat_session(cls, user_names, my_id):
        await asyncio.get_event_loop().run_in_executor(None, partial(cls._create_chat_session, user_names))
        return await cls.get_my_sessions(my_id)

    @classmethod
    async def get_my_sessions(cls, user_id):
        return await asyncio.get_event_loop().run_in_executor(None, partial(cls._get_my_sessions, user_id))