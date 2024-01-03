import logging

from fastapi import APIRouter, Body, HTTPException, status

from app.api.deps import FormDataDep, SessionDep
from app.api.routers.users import user_not_found_exception
from app.api.utils import (
    active_user_exception,
    credentials_exception,
    email_registered_exception,
    inactive_user_exception,
)
from app.core.token_utils import (
    TokenType,
    decode_token,
    generate_password_reset_validation_token,
    generate_registration_validation_token,
    generate_tokens_response,
)
from app.crud.user import crud_user
from app.models.auth import NewPassword, RefreshTokenRequest, TokensResponse
from app.models.msg import Message
from app.models.user import User, UserCreate, UserRecoverPassword, UserUpdatePassword
from app.utils import send_new_account_email, send_reset_password_email, send_test_email

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/access-token")
async def login_access_token(
    session: SessionDep, form_data: FormDataDep
) -> TokensResponse:
    """Get an access token for future requests using email and password."""
    user = await crud_user.authenticate(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    if not user.is_active:
        raise inactive_user_exception
    return generate_tokens_response(user.id)


@router.post("/refresh-token")
async def refresh_token(
    session: SessionDep, token: RefreshTokenRequest
) -> TokensResponse:
    """Get an access token using a refresh token."""
    user_id = decode_token(token.refresh_token, TokenType.REFRESH)
    if session.get(User, user_id):
        return generate_tokens_response(user_id)
    raise credentials_exception


@router.post("/registration")
async def register_user(session: SessionDep, data: UserCreate) -> Message:
    """Register new user."""
    email = data.email
    if user := await crud_user.get_by_email(session, email):
        if user.is_active:
            raise email_registered_exception
    else:
        await crud_user.create(session, data)
    token = generate_registration_validation_token(email)
    send_new_account_email.delay(email, token)
    return Message(msg="New account email sent")


@router.post("/registration/validation")
async def validate_register_user(
    session: SessionDep, token: str = Body(..., embed=True)
) -> Message:
    """Validate registration token and activate the account."""
    email = decode_token(token, TokenType.REGISTER)
    user = await crud_user.get_by_email(session, email)
    if not user:
        raise user_not_found_exception
    if user.is_active:
        raise active_user_exception

    await crud_user.activate(session, user)
    return Message(msg="Account activated successfully")


@router.post("/password-reset")
async def reset_password(session: SessionDep, data: UserRecoverPassword) -> Message:
    """Send password reset email."""
    email = data.email
    user = await crud_user.get_by_email(session, email)
    if not user:
        raise user_not_found_exception
    if not user.is_active:
        raise inactive_user_exception

    token = generate_password_reset_validation_token(email)
    send_reset_password_email.delay(email, token)
    return Message(msg="Password recovery email sent")


@router.post("/password-reset/validation")
async def validate_reset_password(session: SessionDep, body: NewPassword) -> Message:
    """Validate password reset token and reset the password."""
    email = decode_token(body.token, TokenType.PASSWORD_RESET)
    if not email:
        raise credentials_exception
    user = await crud_user.get_by_email(session, email)
    if not user:
        raise user_not_found_exception
    if not user.is_active:
        raise inactive_user_exception

    await crud_user.update(
        session, user, UserUpdatePassword(password=body.new_password)
    )
    return Message(msg="Password updated successfully")


@router.post("/test-email")
async def test_email(data: UserRecoverPassword) -> Message:
    """Register new user."""
    send_test_email.delay(data.email)
    return Message(msg="Test email sent")
