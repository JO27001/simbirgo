import datetime
import uuid

import jwt

from .settings import JWTSettings


class JWTMethods:
    BLACK_LIST_JWT = set()

    def __init__(
        self,
        access_token_public_key: str,
        access_token_private_key: str,
        refresh_token_public_key: str,
        refresh_token_private_key: str,
        access_token_expires: datetime.timedelta,
        refresh_token_expires: datetime.timedelta,
    ) -> None:
        self.access_token_public_key: str = access_token_public_key
        self.access_token_private_key: str = access_token_private_key
        self.refresh_token_public_key: str = refresh_token_public_key
        self.refresh_token_private_key: str = refresh_token_private_key
        self.access_token_expires: datetime.timedelta = access_token_expires
        self.refresh_token_expires: datetime.timedelta = refresh_token_expires

    def issue_access_token(self, user_id: uuid.UUID) -> str:
        access_token = jwt.encode(
            {
                "user_id": str(user_id),
                "exp": int(
                    datetime.datetime.now().timestamp() + self.access_token_expires.total_seconds()
                )
                + 1,
            },
            self.access_token_private_key,
            algorithm="RS256",
        )
        self.remove_from_blacklist(access_token)
        return access_token

    def decode_access_token(self, access_token: str) -> uuid.UUID | None:
        if self.is_token_blacklisted(access_token):
            return None

        try:
            return uuid.UUID(
                jwt.decode(
                    access_token,
                    self.access_token_public_key,
                    algorithms=["RS256"],
                    options={"require": ["user_id"]},
                ).get("user_id")
            )
        except jwt.PyJWTError:
            return None

    def issue_refresh_token(self, user_id: uuid.UUID) -> str:
        return jwt.encode(
            {
                "user_id": str(user_id),
                "exp": int(
                    datetime.datetime.now().timestamp() + self.refresh_token_expires.total_seconds()
                )
                + 1,
            },
            self.refresh_token_private_key,
            algorithm="RS256",
        )

    def decode_refresh_token(self, refresh_token: str) -> uuid.UUID | None:
        try:
            return uuid.UUID(
                jwt.decode(
                    refresh_token,
                    self.refresh_token_public_key,
                    algorithms=["RS256"],
                    options={"require": ["user_id"]},
                ).get("user_id")
            )
        except jwt.PyJWTError:
            return None

    def remove_from_blacklist(self, token: str) -> None:
        try:
            self.BLACK_LIST_JWT.remove(token)
        except KeyError:
            pass

    def add_to_blacklist(self, token: str) -> None:
        self.BLACK_LIST_JWT.add(token)

    def is_token_blacklisted(self, token: str) -> bool:
        return token in self.BLACK_LIST_JWT


def get_jwt_methods(settings: JWTSettings) -> JWTMethods:
    return JWTMethods(
        access_token_private_key=settings.jwt_access_token_private_key,
        access_token_public_key=settings.jwt_access_token_public_key,
        refresh_token_private_key=settings.jwt_refresh_token_private_key,
        refresh_token_public_key=settings.jwt_refresh_token_public_key,
        access_token_expires=settings.jwt_access_token_expires,
        refresh_token_expires=settings.jwt_access_token_expires,
    )
