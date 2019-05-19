from unittest import TestCase
from Crypto.PublicKey.RSA import RsaKey
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
import base64
import secrets
from OpenSSL import crypto


class TestSendSignMessage(TestCase):
    """test class to demo asym encryption and decryption"""

    def setUp(self) -> None:
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)
        self.public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, k)
        self.private_kay = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
        self.skey = secrets.token_urlsafe(128)

    def test_demo1(self):
        # server side encrypt sym key and send key when requested
        # client 1 signs and encrypts message using sym key

        signer = PKCS1_OAEP.new(self.private_kay, hashAlgo=SHA256.new())
        signer.
        msg = base64.b64encode(self.public_key).decode()
        self.assertNotEqual(msg, self.public_key)


        # client side receives key and decrypts
        key = base64.b64decode(msg)
        self.assertEqual(self.public_key, key)







