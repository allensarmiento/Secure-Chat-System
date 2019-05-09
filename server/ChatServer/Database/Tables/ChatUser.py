from Database.Tables import DeclarativeBase, ChatUserTokens
from sqlalchemy import Column, Integer, String, LargeBinary, Binary
from sqlalchemy.types import LargeBinary
import bcrypt
from OpenSSL import crypto
from Database import DatabaseManager
import asyncio
from functools import partial
from sqlalchemy.orm import relationship
from aiohttp import web
import base64
import hashlib


class ChatUser(DeclarativeBase.Base):
    __tablename__ = 'chatusers'

    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    user_name = Column(String, unique=True, nullable=False, index=True)
    user_password = Column(LargeBinary, nullable=False)
    user_public_key = Column(Binary, nullable=False)

    object_user_tokens = relationship("ChatUserTokens", cascade="save-update,merge,delete,delete-orphan",
                                      uselist=True,
                                      back_populates="object_user")

    def __init__(self, user_id: int, user_name: str, user_pass: str):
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = base64.encodebytes(bcrypt.hashpw(user_pass.encode("utf-8"), b'$2b$12$RhUW67z9C.vlzlIU3ED68O'))  # todo remove me
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)
        self.user_public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, k)
        with open("user_private_key_{}.pem".format(self.user_id), 'wb') as f:
            f.write((crypto.dump_privatekey(crypto.FILETYPE_PEM, k)))
            print("Generated private key for user: {}. Make sure to delete this key from the server after distributing it.".format(self.user_id))

    def get_id(self) -> int:
        return self.user_id

    def get_name(self) -> str:
        return self.user_name

    def test_password(self, input_password_encrypted: str):
        """Returns true if the user password matches db pass, else false"""
        try:
            user_pass = base64.b64decode(self.user_password)
            input_pass = base64.b64decode(input_password_encrypted)
            return user_pass == input_pass

        except:
            return False

    def __str__(self):
        return "ID: {} Name: {}".format(self.user_id, self.user_name)

    @classmethod
    def _get_user_byid(cls, user_id):
        db = DatabaseManager.DatabaseManager.get_session()
        try:
            return db.query(cls).filter(cls.user_id == user_id).one_or_none()
        finally:
            db.close()

    @classmethod
    def _get_user_byname(cls, user_name):
        db = DatabaseManager.DatabaseManager.get_session()
        try:
            return db.query(cls).filter(cls.user_name == user_name).one_or_none()
        finally:
            db.close()

    @classmethod
    def _generate_token(cls, user_id):
        db = DatabaseManager.DatabaseManager.get_session()
        try:
            user = cls._get_user_byid(user_id)
            if not user:
                raise web.HTTPNotFound(reason="User not found.")
            else:
                token = ChatUserTokens.ChatUserTokens(user.get_id())
                db.add(token)
                db.commit()
                return token.token
        except Exception as ex:
            raise web.HTTPServerError(reason=str(ex))
        finally:
            db.close()

    @classmethod
    async def get_user(cls, user_id):
        return await asyncio.get_event_loop().run_in_executor(None, partial(cls._get_user_byid, user_id))

    @classmethod
    async def get_user_byname(cls, user_name):
        return await asyncio.get_event_loop().run_in_executor(None, partial(cls._get_user_byname, user_name))

    @classmethod
    async def generate_token(cls, user_id) -> str:
        return await asyncio.get_event_loop().run_in_executor(None, partial(cls._generate_token, user_id))

