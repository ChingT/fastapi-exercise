from datetime import datetime

from pydantic import ConfigDict
from sqlmodel import SQLModel


class RefreshTokenRequest(SQLModel):
    refresh_token: str


class TokensResponse(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    token_type: str = "bearer"
    access_token: str
    refresh_token: str


class JWTTokenPayload(SQLModel):
    sub: str | int
    exp: datetime
    nbf: datetime
    type: str


class NewPassword(SQLModel):
    token: str
    new_password: str
