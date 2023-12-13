from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokensResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token_type: str
    access_token: str
    refresh_token: str


class JWTTokenPayload(BaseModel):
    sub: str | int
    exp: datetime
    nbf: datetime
    refresh: bool
