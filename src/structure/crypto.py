from ecdsa import SigningKey
from ecdsa import VerifyingKey
from ecdsa import BadSignatureError
import os
import binascii


class Crypto():
    """
    This class encapsulate the ecdsa library
    """
    def __init__(self, path=os.getcwd()):
        """
        We load in the constructor the private and the public key
        """
        # We create the path for the private and the public key in the hard
        # drive
        private_path = os.path.normpath(os.path.join(path, "private.pem"))
        public_path = os.path.normpath(os.path.join(path, "public.pem"))

        # We get (or generate) the private key
        if(os.path.exists(private_path)):
            private_file = open(private_path, "rb")
            self.private = SigningKey.from_pem(private_file.read())
            private_file.close()
        else:
            self.private = SigningKey.generate()
            private_file = open(private_path, "wb")
            private_file.write(self.private.to_pem())
            private_file.close()

        # We get (or generate) the public key
        if(os.path.exists(public_path)):
            public_file = open(public_path, "rb")
            self.public = VerifyingKey.from_pem(public_file.read())
            public_file.close()
        else:
            self.public = self.private.get_verifying_key()
            public_file = open(public_path, "wb")
            public_file.write(self.public.to_pem())
            public_file.close()

    def get_public(self):
        """
        We get the public key
        """
        return binascii.hexlify(self.public.to_string()).decode("utf-8")

    def sign(self, message):
        """
        The function sign a message
        """
        # We turn the message into bytes if the message is in string
        if isinstance(message, str):
            message = message.encode("utf-8")
        return binascii.hexlify(self.private.sign(message)).decode("utf-8")

    def verify(public, signature, message):
        """
        The function verify if a signature correspond to a message
        """
        # We turn the message into bytes if the message is in string
        if isinstance(message, str):
            message = message.encode("utf-8")

        # We transform the signature in a signature with bytes
        if isinstance(signature, str):
            signature = binascii.unhexlify(signature)

        # We create an object for the public key
        public = binascii.unhexlify(public)
        public = VerifyingKey.from_string(public)

        # We verify the key
        try:
            public.verify(signature, message)
            return True
        except BadSignatureError:
            return False
