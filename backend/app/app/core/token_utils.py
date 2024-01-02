import datetime
from enum import Enum

from jose import JWTError, jwt

from app.core.config import settings
from app.models.auth import JWTTokenPayload, TokensResponse

JWT_ALGORITHM = "HS256"


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    REGISTER = "register"
    PASSWORD_RESET = "password-reset"


def generate_tokens_response(subject: str | int) -> TokensResponse:
    """Generate tokens and return AccessTokenResponse."""
    access_token = create_token(
        subject, settings.ACCESS_TOKEN_EXPIRE_HOURS, TokenType.ACCESS
    )
    refresh_token = create_token(
        subject, settings.REFRESH_TOKEN_EXPIRE_HOURS, TokenType.REFRESH
    )
    return TokensResponse(access_token=access_token, refresh_token=refresh_token)


def create_token(sub: str | int, exp_hours: float, type: TokenType) -> str:
    """Create jwt access or refresh token for user.

    Args:
    ----
        sub: anything unique to user, id or email etc. Need to be converted to a string.
        exp_hours: expire time in hours.
        type: token type.
    """
    now = datetime.datetime.now(tz=datetime.UTC)
    exp = now + datetime.timedelta(hours=exp_hours)

    claims = {**JWTTokenPayload(sub=str(sub), exp=exp, nbf=now, type=type).model_dump()}
    return jwt.encode(claims, settings.SECRET_KEY, JWT_ALGORITHM)


def decode_token(token: str, type: TokenType) -> str:
    """Decode JWT token and return the subject."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None

    token_data = JWTTokenPayload(**payload)
    if type.value != token_data.type:
        return None

    return token_data.sub


def generate_registration_validation_token(email: str) -> str:
    """Create registration validation token with email as subject."""
    return create_token(
        email, settings.EMAIL_VALIDATION_TOKEN_EXPIRE_HOURS, TokenType.REGISTER
    )


def generate_password_reset_validation_token(email: str) -> str:
    """Create password reset validation token with email as subject."""
    return create_token(
        email, settings.EMAIL_VALIDATION_TOKEN_EXPIRE_HOURS, TokenType.PASSWORD_RESET
    )
