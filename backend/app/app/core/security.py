from passlib.context import CryptContext

from app.core.config import settings

PWD_CONTEXT = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.SECURITY_BCRYPT_ROUNDS,
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain and hashed password matches.

    Applies passlib context based on bcrypt algorithm on plain passoword.
    It takes about 0.3s for default 12 rounds of SECURITY_BCRYPT_DEFAULT_ROUNDS.
    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Create hash from password.

    Applies passlib context based on bcrypt algorithm on plain passoword.
    It takes about 0.3s for default 12 rounds of SECURITY_BCRYPT_DEFAULT_ROUNDS.
    """
    return PWD_CONTEXT.hash(password)
