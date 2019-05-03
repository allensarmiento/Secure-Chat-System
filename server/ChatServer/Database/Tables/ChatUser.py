from ChatServer.Database.Tables import DeclarativeBase
from sqlalchemy import Column, Integer, String, LargeBinary
import bcrypt
from OpenSSL import crypto


class ChatUser(DeclarativeBase.Base):
    __tablename__ = 'chatusers'

    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    user_name = Column(String, default="", nullable=False, index=True)
    user_password = Column(String, nullable=False)
    user_public_key = Column(LargeBinary, nullable=False)

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

    def test_password(self, input_password: str):
        """Returns true if the user password matches db pass, else false"""
        return bcrypt.checkpw(input_password.encode('utf-8'), self.user_password)

    def __str__(self):
        return "ID: {} Name: {}".format(self.user_id, self.user_name)

