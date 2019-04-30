from ChatServer.Utilities import Singleton
from ChatServer.Database import DatabaseInit
from sqlalchemy.orm import Session


class DatabaseManager(metaclass=Singleton.Singleton):
    def __init__(self, memory_db=False):
        self.db = DatabaseInit.DatabaseInit(memory_db)

    def db_init(self):
        self.db.setup_db()

    def _get_session(self) -> Session:
        return self.db.get_session()

    @classmethod
    def get_session(cls) -> Session:
        db = cls()
        return db._get_session()
