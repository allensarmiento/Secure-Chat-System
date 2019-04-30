from ChatServer.Database import DatabaseManager


class Main(object):
    @classmethod
    def main(cls):
        db_manage = DatabaseManager.DatabaseManager()
        db_manage.db_init()


if __name__=="__main__":
    Main.main()
