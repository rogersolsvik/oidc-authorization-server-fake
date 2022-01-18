import logging
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from logging import Logger


class KeyStore:
    __private_key: rsa.RSAPrivateKey

    def __init__(self, logger: Logger):
        logger.debug("Initializing KeyStore and generating key-pair")
        self.__private_key = rsa.generate_private_key(0x10001, 2048)

        logger.debug(f"Private key (PEM):\n {self.private_key_pem.decode('UTF-8')}")
        logger.debug(f"Public key (PEM):\n {self.public_key_pem.decode('UTF-8')}")

    @property
    def private_key(self):
        return self.__private_key

    @property
    def private_key_pem(self) -> bytes:
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

    @property
    def public_key(self):
        return self.private_key.public_key()

    @property
    def public_key_pem(self) -> bytes:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1
        )
