"""Initialization of module either for blueprint routes or cli (future)"""
from logging import Logger
import flask
from flask import Blueprint, Config
from keystore import KeyStore


from token_generation.token_factory import TokenFactory


def create_routes(config: Config, keystore: KeyStore, logger: Logger):
    """Setup Blueprint routes"""
    blueprint = Blueprint("token", __name__, url_prefix="/token")
    issuer = config.get("OIDC_ISSUER")
    audience = config.get("OIDC_AUDIENCE")
    logger.debug(
        f"Setting up token routes using configured issuer: {issuer} and audience: {audience}"
    )
    token_factory = TokenFactory(keystore)

    @blueprint.route("", methods=["POST"])
    def free_token():
        request_data = flask.request.get_json()
        claims = request_data.get("claims", {})
        token = token_factory.create_free_token(
            issuer=issuer, audience=audience, claims=claims
        )

        return {"token": token}

    return blueprint
