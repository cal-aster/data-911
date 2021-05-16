import os
from copy import deepcopy
from datetime import datetime, timedelta
from hashlib import sha256
from typing import Callable

import jwt
from fastapi import Depends, HTTPException
from src.models.auth import UserModel
from werkzeug.security import safe_str_cmp


class Authentication:
    def __init__(self, oauth_scheme=None) -> None:
        self.password = os.getenv("JWT_PASSWORD")
        self.username = os.getenv("JWT_USERNAME")
        self.oauth_scheme = oauth_scheme

    def authenticate(self, username: str, password: str) -> UserModel:
        password = sha256(password.encode("utf-8")).hexdigest()
        if safe_str_cmp(username, self.username) and safe_str_cmp(
            password, self.password
        ):
            return UserModel(**{"id": self.username})

    def identity(self, packet: dict) -> UserModel:
        if safe_str_cmp(packet.get("identity"), self.username):
            return UserModel(**{"id": self.username})

    def create_token(self, data: dict) -> str:
        payload = deepcopy(data)
        duration = timedelta(seconds=int(os.getenv("JWT_EXPIRATION_DELTA")))
        expiration = datetime.utcnow() + duration
        payload.update({"exp": expiration})
        return jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")

    def verify(self) -> Callable:
        def verify_payload(token: str = Depends(self.oauth_scheme)) -> UserModel:
            try:
                user: UserModel = self.identity(
                    jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
                )
                if user is None:
                    raise HTTPException(
                        status_code=401,
                        detail="Invalid credentials",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                return user
            except Exception:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        return verify_payload
