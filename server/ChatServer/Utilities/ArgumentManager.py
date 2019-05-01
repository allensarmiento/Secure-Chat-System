from ChatServer.Utilities import Singleton
import argparse


class ArgumentManager(metaclass=Singleton.Singleton):
    def __init__(self):
        args = argparse.ArgumentParser()
        args.add_argument("--key", "-k",
                            help="Specify the encrypted column decryption key.",
                            default="TestKeyDoNotUse")
        self.args = args.parse_args()

    @classmethod
    def get_db_key(cls):
        am = cls()
        key = am.args.key
        if key == "TestKeyDoNotUse":
            print("You should specify a key to use to encrypt the database columns by starting "
                  "the application with python3 ChatServer --key KeyHere")
        return key

