"""Initialization of module either for blueprint routes or cli (future)"""
import flask
from flask import Blueprint, Config
from keystore import KeyStore


from token_generation.token_factory import TokenFactory


def create_routes(config: Config, keystore: KeyStore):
    """Setup Blueprint routes"""
    blueprint = Blueprint("token", __name__, url_prefix="/token")
    token_factory = TokenFactory(keystore)
    issuer = config.get("OIDC_ISSUER")
    audience = config.get("OIDC_AUDIENCE")

    @blueprint.route("", methods=["POST"])
    def free_token():
        request_data = flask.request.get_json()
        claims = request_data.get("claims", {})
        token = token_factory.create_free_token(
            issuer=issuer, audience=audience, **claims
        )

        return {**token}

    return blueprint
