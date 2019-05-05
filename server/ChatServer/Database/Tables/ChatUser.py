from Database.Tables import DeclarativeBase
from sqlalchemy import Column, Integer, String, LargeBinary, Binary
import bcrypt
from OpenSSL import crypto
from Database import DatabaseManager
import asyncio
from functools import partial
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class ChatUser(DeclarativeBase.Base):
    __tablename__ = 'chatusers'

    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    user_name = Column(String, default="", nullable=False, index=True)
    user_password = Column(Binary, nullable=False)
    user_public_key = Column(Binary, nullable=False)

    def __init__(self, user_id: int, user_name: str, user_pass: str):
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = bcrypt.hashpw(user_pass.encode('utf-8'), bcrypt.gensalt())
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
        return bcrypt.checkpw(input_password_encrypted.encode('utf-8'), self.encrypt_string(self.user_password))

    def encrypt_string(self, decrypted_string):
        key = serialization.load_pem_public_key(self.user_public_key, backend=default_backend())
        return key.encrypt(decrypted_string, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA3_256()),
                                                       algorithm=hashes.SHA3_256(),
                                                       label=None))

    def __str__(self):
        return "ID: {} Name: {}".format(self.user_id, self.user_name)

    @classmethod
    def _get_user(cls, user_id):
        db = DatabaseManager.DatabaseManager.get_session()
        try:
            return db.query(cls).filter(cls.user_id == user_id).one_or_none()
        finally:
            db.close()

    @classmethod
    async def get_user(cls, user_id):
        return await asyncio.get_event_loop().run_in_executor(None, partial(cls._get_user, user_id))

