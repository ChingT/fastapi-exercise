from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


no_permissions_exception = HTTPException(
    status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
)


user_not_found_exception = HTTPException(
    status.HTTP_404_NOT_FOUND, detail="User not found"
)
inactive_user_exception = HTTPException(
    status.HTTP_400_BAD_REQUEST, detail="Inactive user"
)
active_user_exception = HTTPException(
    status.HTTP_400_BAD_REQUEST, detail="User account already activated"
)
email_registered_exception = HTTPException(
    status.HTTP_400_BAD_REQUEST, detail="Email already registered"
)


item_not_found_exception = HTTPException(
    status.HTTP_404_NOT_FOUND, detail="Item not found"
)
