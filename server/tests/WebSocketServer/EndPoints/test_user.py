from unittest import TestCase, skip


class TestUser(TestCase):
    @skip
    def test_get_user(self):
        self.fail()
