import datetime

from jose import JWTError, jwt

from app.core.config import settings
from app.models.auth import JWTTokenPayload, TokensResponse

JWT_ALGORITHM = "HS256"


def generate_tokens_response(subject: str | int) -> TokensResponse:
    """Generate tokens and return AccessTokenResponse."""
    access_token = create_token(subject, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_token(
        subject, settings.REFRESH_TOKEN_EXPIRE_MINUTES, refresh=True
    )
    return TokensResponse(
        token_type="Bearer", access_token=access_token, refresh_token=refresh_token
    )


def create_token(sub: str | int, exp_mins: float, refresh: bool = False) -> str:
    """Create jwt access or refresh token for user.

    Args:
    ----
        sub: anything unique to user, id or email etc. Need to be converted to a string.
        exp_mins: expire time in minutes
        refresh: if True, this is refresh token
    """
    now = datetime.datetime.now(tz=datetime.UTC)
    exp = now + datetime.timedelta(minutes=exp_mins)

    claims = {
        **JWTTokenPayload(sub=str(sub), exp=exp, nbf=now, refresh=refresh).model_dump()
    }
    return jwt.encode(claims, settings.SECRET_KEY, JWT_ALGORITHM)


def decode_token(token: str, is_refresh: bool = False) -> str:
    """Decode JWT token and return the subject."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None

    token_data = JWTTokenPayload(**payload)
    if is_refresh != token_data.refresh:
        return None

    return token_data.sub
