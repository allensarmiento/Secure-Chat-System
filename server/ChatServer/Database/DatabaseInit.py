from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from ChatServer.Database.Tables import DeclarativeBase, ChatUser
import traceback
from sqlalchemy.pool import StaticPool


class DatabaseInit(object):
    def __init__(self, memory_db=False):
        self.db_name = "Database.db"
        if memory_db:
            self.engine = create_engine('sqlite:///', connect_args={'check_same_thread': False}, poolclass=StaticPool)
        else:
            self.engine = create_engine('sqlite:///{}'.format(self.db_name),
                                        connect_args={'check_same_thread': False, 'timeout': 3000}, echo=False)
        DeclarativeBase.Base.metadata.create_all(self.engine)
        self._dbSession = sessionmaker(bind=self.engine)
        self._sc_session = scoped_session(self._dbSession)

    def get_session(self) -> Session:
        return self._sc_session()

    def setup_db(self):
        print("Importing data to the database: '{}'".format(self.db_name))
        db = self.get_session()
        try:
            for i in range(1, 10):
                user = ChatUser.ChatUser(i, "Name{}".format(i), "password{}".format(i))
                print("Adding {} to database.".format(user))
                db.merge(user)
            db.commit()
            print("ok")
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            print("Error when loading data to the database")
        finally:
            db.close()

