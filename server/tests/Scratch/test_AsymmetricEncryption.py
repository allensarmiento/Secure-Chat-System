from unittest import TestCase
from Crypto.PublicKey.RSA import RsaKey
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import secrets


class TestAsymmetricEncryption(TestCase):
    """test class to demo asym encryption and decryption"""

    def setUp(self) -> None:
        key = RSA.generate(2048)
        self.private_key: RsaKey = RSA.import_key(key.export_key("PEM"))
        self.public_key: RsaKey = RSA.import_key(key.publickey().export_key("PEM"))

    def test_demo1(self):
        msg = b'This is a test message'
        cipher = PKCS1_OAEP.new(self.public_key)
        ciphertext = cipher.encrypt(msg)
        send_cipher_text = base64.b64encode(ciphertext)

        recieve_cipher_bin = base64.b64decode(send_cipher_text)
        cipher = PKCS1_OAEP.new(self.private_key)
        message = cipher.decrypt(recieve_cipher_bin)
        self.assertEqual(msg, message)
