from ChatServer.Database.Tables import DeclarativeBase
from sqlalchemy import Column, Integer, String


class ChatUser(DeclarativeBase.Base):
    __tablename__ = 'chatusers'

    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    user_name = Column(String, default="", nullable=False, index=True)

    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def get_id(self) -> int:
        return self.user_id

    def get_name(self) -> str:
        return self.user_name

    def __str__(self):
        return "ID: {} Name: {}".format(self.user_id, self.user_name)
