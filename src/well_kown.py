"""Route setup for well-known"""
from cryptography.hazmat.primitives import serialization
from flask import Blueprint
from flask.config import Config
from flask.helpers import url_for
from authlib.jose import JsonWebKey

from keystore import KeyStore


def create_routes(config: Config, keystore: KeyStore) -> Blueprint:
    """Register paths for well-known configuration"""
    blueprint = Blueprint("well-known", __name__, url_prefix="/.well-known")
    __jwk = JsonWebKey.import_key(
        keystore.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1,
        ),
    )

    @blueprint.route("/openid-configuration")
    def openid_configuration():
        issuer = config.get("OIDC_ISSUER")
        return {
            "issuer": issuer,
            "jwks_uri": f"{issuer}{url_for('well-known.jwks')}",
            "token_endpoint": f"{issuer}/token",
            "grant_types_supported": ["client_credentials"],
            "response_types_supported": ["token"],
            "token_endpoint_auth_methods_supported": ["client_secret_post"],
            "id_token_signing_alg_values_supported": ["RS256"],
            "subject_types_supported": ["public"],
        }

    @blueprint.route("/jwks")
    def jwks():
        return {
            "keys": [{"use": "sig", "kty": "RSA", **__jwk}],
        }

    return blueprint
