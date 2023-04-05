from passlib.context import CryptContext
from os import urandom

DEFAULT_DATABASE_NAME = "backend_users"

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
        )

SECRET_KEY = urandom(16)
