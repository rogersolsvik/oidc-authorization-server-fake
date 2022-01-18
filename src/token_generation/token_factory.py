"""The token factory creates and signs tokens"""
import time
from datetime import timedelta, datetime
from authlib.jose import jwt
from keystore import KeyStore


class TokenFactory:
    def __init__(self, keystore: KeyStore):
        self._keystore = keystore

    def create_free_token(self, issuer: str, audience: str, claims: dict) -> str:
        """Create a new free-form token. That means defining the claims you like"""
        now = datetime.now()
        expiry = now + timedelta(minutes=60)
        payload = {
            "aud": audience,
            "iss": issuer,
            "iat": int(round(now.timestamp())),
            "exp": int(round(expiry.timestamp())),
            **claims,  # The above claims will be overwritten if they are provided in `claims`
        }
        header = {"alg": "RS256"}

        encoded_token = jwt.encode(header, payload, self._keystore.private_key)
        return encoded_token.decode("utf-8")
