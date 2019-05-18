from unittest import TestCase
from Crypto.PublicKey.RSA import RsaKey
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import secrets
from OpenSSL import crypto


class TestSymmetricEncryption(TestCase):
    """test class to demo asym encryption and decryption"""

    def setUp(self) -> None:
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)
        self.public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, k)
        self.private_kay = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
        self.skey = secrets.token_urlsafe(128)

    def test_encrypt_skey(self):
        # server side encrypt sym key and send key when requested
        cipher = PKCS1_OAEP.new(RSA.import_key(self.public_key))
        msg = self.skey.encode()
        symmetric_key = base64.b64encode(cipher.encrypt(msg)).decode()
        self.assertNotEqual(symmetric_key, self.skey)
        print("Original symm key: '{}'".format(self.skey))
        print("Sent encrypted key using user public key: '{}'".format(symmetric_key))

        # client side receives key and decrypts
        print("Private key: {}".format(self.private_kay.decode()))
        cipher = PKCS1_OAEP.new(RSA.import_key(self.private_kay))
        symmetric_key = cipher.decrypt(base64.b64decode(symmetric_key)).decode()
        self.assertEqual(self.skey, symmetric_key)







