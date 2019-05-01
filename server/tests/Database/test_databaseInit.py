from tests.AbstractTestBase import TestBase
from ChatServer.Database import DatabaseInit
from sqlalchemy.orm import Session
from ChatServer.Database.Tables import ChatUser


class TestDatabaseInit(TestBase.TestBase):
    def setUp(self) -> None:
        self.db = DatabaseInit.DatabaseInit(memory_db=True)

    def test_get_session(self):
        s = self.db.get_session()
        self.assertIsInstance(s, Session)

    def test_setup_db(self):
        self.db.setup_db()
        db = self.db.get_session()
        r = db.query(ChatUser.ChatUser).all()
        self.assertEqual(9, len(r))
        index = 1
        for u in r:
            self.assertIsInstance(u, ChatUser.ChatUser)
            self.assertEqual(index, u.get_id())
            self.assertIsInstance(u.get_id(), int)
            self.assertEqual("Name{}".format(index), u.get_name())
            self.assertTrue(u.test_password("password{}".format(index)))
            index += 1

