from os import environ
from flask import Flask
import config
from keystore import KeyStore
from well_kown import create_routes as create_well_known_routes
from token_generation import create_routes as create_token_routes


def create_app():
    """Server factory"""
    app = Flask(__name__)
    app.config.from_object(config)
    keystore = KeyStore()
    if __name__ == "__main__":
        app.run(port=environ.get("PORT"))

    app.register_blueprint(create_well_known_routes(app.config, keystore))
    app.register_blueprint(create_token_routes(app.config, keystore))

    return app
