from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from starlette.requests import Request
from pydantic import BaseModel


class CurrentUser(BaseModel):
    """Placeholder user object for auth."""
    role: str = "operator"


security = HTTPBearer(auto_error=False)


async def require_operator(
    credentials = Depends(security),
) -> CurrentUser:
    """
    Placeholder authentication dependency.
    
    TODO Phase 7: Implement JWT validation here. For now, we accept
    any well-formed Bearer token and return a placeholder user.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Phase 4: Accept the token shape; Phase 7 will validate JWT
    return CurrentUser(role="operator")
