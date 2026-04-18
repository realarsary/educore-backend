from fastapi import HTTPException, status, Depends

from app.api.deps import get_current_user
from app.core.roles import UserRole


def require_role(*allowed_roles: UserRole):
    def wrapper(user=Depends(get_current_user)):

        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        return user

    return wrapper


def require_owner_or_role(check_owner_fn, *allowed_roles):
    def wrapper(user=Depends(get_current_user)):
        if user.role in allowed_roles:
            return user

        if check_owner_fn(user):
            return user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return wrapper