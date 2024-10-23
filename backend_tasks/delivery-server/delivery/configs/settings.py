from .base import *

ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")

# Redis settings
REDIS_EXPIRATION_TIME = os.environ.get("REDIS_EXPIRATION_TIME", 3600)
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

# Token settings
ACCESS_TOKEN_EXPIRE_TIME = os.environ.get("ACCESS_TOKEN_EXPIRE_TIME", 3600)
REFRESH_ACCESS_TOKEN_EXPIRE_TIME = os.environ.get(
    "REFRESH_ACCESS_TOKEN_EXPIRE_TIME", 3600 * 24
)
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET", "access-token-secret")
REFRESH_TOKEN_SECRET = os.environ.get("REFRESH_TOKEN_SECRET", "refresh-token-secret")

# S3 settings

S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL", "http://localhost")
S3_PORT = os.environ.get("S3_PORT", 8333)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "admin")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "password")

# Swagger Setting
SPECTACULAR_SETTINGS = {
    "TITLE": "App API",
    "DESCRIPTION": "App API for Delivery App",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SCHEMA_PATH_PREFIX": "/api/v1",
    "SCHEMA_PATH_PREFIX_TRIM": False,
    "COMPONENT_SPLIT_REQUEST": True,
}
JWT_SECRET_KEY = os.environ.get("JWT_SECRET", "jwt-secret")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_TIME = os.environ.get("JWT_EXPIRE_TIME", 3600)

AUTH_USER_MODEL = "delivery.User"
