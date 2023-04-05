#!/usr/bin/env python3

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"],
                           deprecated="auto",
                           )
hash = pwd_context.hash("testme")
print(hash)
