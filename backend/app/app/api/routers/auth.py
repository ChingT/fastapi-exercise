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
from app.models.auth import RefreshTokenRequest, TokensResponse
from app.models.msg import Msg
from app.models.user import User, UserCreate, UserRecoverPassword, UserUpdatePassword
from app.utils import send_new_account_email, send_reset_password_email

router = APIRouter()


@router.post("/access-token", status_code=status.HTTP_201_CREATED)
def login_access_token(db: SessionDep, form_data: FormDataDep) -> TokensResponse:
    """Get an access token for future requests using email and password."""
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    if not user.is_active:
        raise inactive_user_exception
    return generate_tokens_response(user.id)


@router.post("/refresh-token", status_code=status.HTTP_201_CREATED)
def refresh_token(db: SessionDep, token: RefreshTokenRequest) -> TokensResponse:
    """Get an access token using a refresh token."""
    user_id = decode_token(token.refresh_token, TokenType.REFRESH)
    if db.get(User, user_id):
        return generate_tokens_response(user_id)
    raise credentials_exception


@router.post("/registration")
def register_user(db: SessionDep, data: UserCreate) -> Msg:
    """Register new user."""
    email = data.email
    if crud_user.get_by_email(db, email=email):
        raise email_registered_exception

    crud_user.create(db, obj_in=data)
    token = generate_registration_validation_token(email=email)
    send_new_account_email(email, token)
    return {"msg": "New account email sent"}


@router.post("/registration/validation")
def validate_register_user(db: SessionDep, token: str = Body(..., embed=True)) -> Msg:
    """Validate registration token and activate the account."""
    email = decode_token(token, TokenType.REGISTER)
    user = crud_user.get_by_email(db, email=email)
    if not user:
        raise user_not_found_exception
    if user.is_active:
        raise active_user_exception

    crud_user.activate(db, user)
    return {"msg": "Account activated successfully"}


@router.post("/password-reset")
def reset_password(db: SessionDep, data: UserRecoverPassword) -> Msg:
    """Send password reset email."""
    email = data.email
    user = crud_user.get_by_email(db, email=email)
    if not user:
        raise user_not_found_exception
    if not user.is_active:
        raise inactive_user_exception

    token = generate_password_reset_validation_token(email=email)
    send_reset_password_email(email, token)
    return {"msg": "Password recovery email sent"}


@router.post("/password-reset/validation")
def validate_reset_password(
    db: SessionDep, token: str = Body(...), new_password: str = Body(...)
) -> Msg:
    """Validate password reset token and reset the password."""
    email = decode_token(token, TokenType.PASSWORD_RESET)
    if not email:
        raise credentials_exception
    user = crud_user.get_by_email(db, email=email)
    if not user:
        raise user_not_found_exception
    if not user.is_active:
        raise inactive_user_exception

    crud_user.update(db, db_obj=user, obj_in=UserUpdatePassword(password=new_password))
    return {"msg": "Password updated successfully"}
