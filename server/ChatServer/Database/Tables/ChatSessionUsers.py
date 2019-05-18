from Database.Tables import DeclarativeBase, ChatUser
from sqlalchemy import Column, Integer, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
import secrets
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
import base64


class ChatSessionUsers(DeclarativeBase.Base):
    __tablename__ = 'chatsessionusers'

    chat_session_id = Column(Integer, ForeignKey("chatsessions.channel_id"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("chatusers.user_id"), primary_key=True, nullable=False)
    symmetric_key = Column(LargeBinary, nullable=False)  # key encrypted using user's public key and base 64 encoded

    object_chat_session = relationship("ChatSessions", uselist=False, back_populates="object_session_users")
    object_user = relationship("ChatUser", uselist=False, back_populates="object_user_chat_sessions")


    def __init__(self, chat_session, chat_user: ChatUser.ChatUser, symmetric_key):
        self.object_chat_session = chat_session
        self.user_id = chat_user.get_id()
        cipher = PKCS1_OAEP.new(RSA.import_key(chat_user.user_public_key))
        msg = symmetric_key.encode()
        self.symmetric_key = base64.b64encode(cipher.encrypt(msg))

    def get_key(self):
        return self.symmetric_key.decode("utf-8")

