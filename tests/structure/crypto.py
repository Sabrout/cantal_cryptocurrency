import unittest
from src.structure.crypto import Crypto


class CryptoTest(unittest.TestCase):

    def test_signature(self):
        c = Crypto()
        sign = c.sign("test")
        test = Crypto.verify(c.get_public(), sign, "test")
        print(c.get_public())
        print(sign)
        self.assertEqual(test, True)
