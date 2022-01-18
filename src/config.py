"""General application configuration"""
import os

OIDC_ISSUER = os.environ.get("OIDC_ISSUER", default="http://localhost:8080")
OIDC_AUDIENCE = os.environ.get("OIDC_AUDIENCE", default="http://localhost:8080")
