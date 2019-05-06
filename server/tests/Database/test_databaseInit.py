from tests.AbstractTestBase import TestBase
from Database import DatabaseInit
from sqlalchemy.orm import Session
from Database.Tables import ChatUser
import bcrypt
import base64

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
            password = bcrypt.hashpw(("password{}".format(index)).encode('utf-8'), b'$2b$12$RhUW67z9C.vlzlIU3ED68O')  # todo remove me
            password = base64.b64encode(password)
            self.assertTrue(u.test_password(password))
            index += 1

