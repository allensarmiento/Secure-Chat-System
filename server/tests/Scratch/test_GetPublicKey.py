from unittest import TestCase
from Crypto.PublicKey.RSA import RsaKey
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import secrets
from OpenSSL import crypto


class TestGetPublicKey(TestCase):
    """test class to demo asym encryption and decryption"""

    def setUp(self) -> None:
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)
        self.public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, k)
        self.private_kay = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)

    def test_key_key(self):
        # server side encrypt sym key and send key when requested
        self.assertIsInstance(self.public_key, bytes)

        msg = base64.b64encode(self.public_key).decode()
        self.assertNotEqual(msg, self.public_key)


        # client side receives key and decrypts
        key = base64.b64decode(msg)
        self.assertEqual(self.public_key, key)







