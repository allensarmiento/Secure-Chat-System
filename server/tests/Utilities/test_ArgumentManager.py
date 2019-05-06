from tests.AbstractTestBase import TestBase
from Utilities import ArgumentManager
import sys


class TestArgumentManager(TestBase.TestBase):
    def setUp(self) -> None:
        sys.argv = [sys.argv[0]]
        sys.argv.extend(['--key', "ThisIsATestKey"])

    def test_get_db_key(self):
        self.assertEqual("ThisIsATestKey", ArgumentManager.ArgumentManager.get_db_key())
