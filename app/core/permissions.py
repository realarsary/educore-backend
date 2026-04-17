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