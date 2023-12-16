from fastapi import APIRouter, Body, HTTPException, status

from app.api.deps import FormDataDep, SessionDep
from app.api.routers.users import user_not_found_exception
from app.api.utils import (
    credentials_exception,
    email_registered_exception,
    inactive_user_exception,
)
from app.core.token_utils import decode_token, generate_tokens_response
from app.crud.user import crud_user
from app.models.auth import RefreshTokenRequest, TokensResponse
from app.models.msg import Msg
from app.models.user import (
    User,
    UserCreate,
    UserOut,
    UserRecoverPassword,
    UserUpdatePassword,
)
from app.utils import (
    generate_password_reset_token,
    send_new_account_email,
    send_reset_password_email,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/access-token", status_code=status.HTTP_201_CREATED)
def login_access_token(db: SessionDep, form_data: FormDataDep) -> TokensResponse:
    """Get an access token for future requests using username and password."""
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
    user_id = decode_token(token.refresh_token, is_refresh=True)
    if db.get(User, user_id):
        return generate_tokens_response(user_id)
    raise credentials_exception


@router.post("/registration")
def register_user(db: SessionDep, user_in: UserCreate) -> UserOut:
    """Register new user."""
    if crud_user.get_by_email(db, email=user_in.email):
        raise email_registered_exception
    user = crud_user.create(db, obj_in=user_in)
    send_new_account_email(email_to=user_in.email)
    return user


@router.post("/password-recovery")
def recover_password(db: SessionDep, data: UserRecoverPassword) -> Msg:
    """Password Recovery."""
    email = data.email
    user = crud_user.get_by_email(db, email=email)
    if not user:
        raise user_not_found_exception
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(email_to=email, token=password_reset_token)
    return {"msg": "Password recovery email sent"}


@router.post("/password-reset")
def reset_password(
    db: SessionDep, token: str = Body(...), new_password: str = Body(...)
) -> Msg:
    """Reset password."""
    email = verify_password_reset_token(token)
    if not email:
        raise credentials_exception
    user = crud_user.get_by_email(db, email=email)
    if not user:
        raise user_not_found_exception
    if not user.is_active:
        raise inactive_user_exception
    crud_user.update(db, db_obj=user, obj_in=UserUpdatePassword(password=new_password))
    return {"msg": "Password updated successfully"}
