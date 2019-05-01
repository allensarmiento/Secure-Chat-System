from ChatServer.Database.Tables import DeclarativeBase
from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from ChatServer.Utilities import ArgumentManager


class ChatUser(DeclarativeBase.Base):
    __tablename__ = 'chatusers'

    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    user_name = Column(String, default="", nullable=False, index=True)
    user_password = Column(EncryptedType(String, ArgumentManager.ArgumentManager.get_db_key, AesEngine, 'pkcs5'), nullable=False)
    user_public_key = Column(EncryptedType(String, ArgumentManager.ArgumentManager.get_db_key, AesEngine, 'pkcs5'), nullable=False)

    def __init__(self, user_id, user_name, user_pass):
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = user_pass
        self.user_public_key = "fixme"  # todo generate key pair

    def get_id(self) -> int:
        return self.user_id

    def get_name(self) -> str:
        return self.user_name

    def test_password(self, input_password):
        """Returns true if the user password matches db pass, else false"""
        return input_password == self.user_password

    def __str__(self):
        return "ID: {} Name: {}".format(self.user_id, self.user_name)

