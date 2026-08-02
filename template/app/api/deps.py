import logging
from collections.abc import AsyncGenerator, Callable
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.schemas.token import TokenPayload
from app.services.oidc import oidc_provider

logger = logging.getLogger(__name__)

# --- Swagger UI Integration ---
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=oidc_provider.auth_url,
    tokenUrl=oidc_provider.token_url,
)


# --- Base Identity Dependency ---
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenPayload:
    """Intercepts, verifies, and decodes the incoming OIDC access token."""
    try:
        payload = oidc_provider.verify_token(token)

        # 'sub' (Subject) is the OIDC standard for the unique user ID
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing 'sub' (subject) claim.",
            )

        logger.info(f"🔒 Token VERIFIED securely for user: {user_id}")

        # Attach the raw_token so downstream role checks can use it for UserInfo calls
        return TokenPayload(**payload, raw_token=token)

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except RuntimeError as e:
        logger.error(f"Server configuration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server configuration error",
        )


# --- RBAC Dependency Factory ---
def require_role(required_role: str) -> Callable:
    """
    Factory to create a dependency checking for a specific role.
    Usage: @router.get("/admin", dependencies=[Depends(require_role("admin"))])
    """

    async def role_checker(
        current_user: Annotated[TokenPayload, Depends(get_current_user)],
    ) -> TokenPayload:

        # Ask the provider for the user's roles
        user_roles = await oidc_provider.get_user_roles(
            access_token=current_user.raw_token, uid=current_user.sub
        )

        if required_role not in user_roles:
            logger.warning(
                f"🚨 403: User {current_user.sub} attempted action requiring '{required_role}'. "
                f"Current roles: {user_roles}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' is required to perform this action.",
            )

        return current_user

    return role_checker


# --- DB Session Dependency ---
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session for request-scoped dependencies."""
    async with AsyncSessionLocal() as session:
        yield session
