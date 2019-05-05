from Database import DatabaseManager
from WebSocketServer import WebSocketServer


class Main(object):
    @classmethod
    def main(cls):
        db_manage = DatabaseManager.DatabaseManager()
        db_manage.db_init()
        WebSocketServer.WebSocketServer.start_server()


if __name__=="__main__":
    Main.main()
