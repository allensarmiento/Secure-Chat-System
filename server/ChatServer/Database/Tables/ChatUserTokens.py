from Database.Tables import DeclarativeBase, ChatUser
from sqlalchemy import Column, Integer, String, LargeBinary, Binary, ForeignKey
from sqlalchemy.orm import relationship
import asyncio
from functools import partial
import secrets
from Database import DatabaseManager
from aiohttp import web
import traceback


class ChatUserTokens(DeclarativeBase.Base):
    __tablename__ = 'usertokens'

    token = Column(String, primary_key=True, nullable=False, autoincrement=False)
    user_id = Column(Integer, ForeignKey("chatusers.user_id"), nullable=False)

    object_user = relationship("ChatUser", uselist=False, back_populates="object_user_tokens")

    def __init__(self, user_id: int):
        self.token = secrets.token_urlsafe(128)
        self.user_id = user_id

    @classmethod
    def _get_user(cls, token):
        db = DatabaseManager.DatabaseManager.get_session()
        try:
            row = db.query(cls).filter(cls.token == token).one_or_none()
            if not row:
                return None
            else:
                return row.object_user
        except Exception as ex:
            traceback.print_exc()
            raise web.HTTPServerError(reason=str(ex))
        finally:
            db.close()

    @classmethod
    def _token_valid(cls, token):
        db = DatabaseManager.DatabaseManager.get_session()
        try:
            if db.query(cls).filter(cls.token == token).one_or_none():
                return True
            else:
                return False
        except Exception as ex:
            traceback.print_exc()
            raise ex
        finally:
            db.close()

    @classmethod
    async def get_user(cls, token):
        return await asyncio.get_event_loop().run_in_executor(None, partial(cls._get_user, token))

    @classmethod
    async def token_valid(cls, token):
        return await asyncio.get_event_loop().run_in_executor(None, partial(cls._token_valid, token))

