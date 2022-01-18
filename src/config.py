"""General application configuration"""
from email.policy import default
import os

OIDC_ISSUER = os.environ.get("OIDC_ISSUER", default="http://localhost:8080")
OIDC_AUDIENCE = os.environ.get("OIDC_AUDIENCE", default="http://localhost:8080")
DEBUG = os.environ.get("DEBUG", default="False").lower() == "true"
