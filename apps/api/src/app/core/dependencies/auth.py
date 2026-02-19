"""FastAPI dependency injection for JWT authentication and authorization."""

from fastapi import Depends, HTTPException, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
from jose import jwt, JWTError, ExpiredSignatureError

from app.modules.identity.domain.jwt_service import JWTService
from app.core.config import settings


security = HTTPBearer(
    scheme_name="Bearer",
    description="JWT Bearer token"
)


class CurrentUser:
    """Context object for authenticated user from JWT claims."""
    
    def __init__(
        self,
        user_id: UUID,
        tenant_id: UUID,
        roles: list[str],
        iat: int,
        exp: int,
    ):
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.roles = roles
        self.iat = iat
        self.exp = exp
    
    def has_role(self, role: str) -> bool:
        """Check if user has specific role."""
        return role in self.roles
    
    def has_any_role(self, roles: list[str]) -> bool:
        """Check if user has any of the specified roles."""
        return any(role in self.roles for role in roles)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUser:
    """
    Extract and validate JWT from Authorization header.
    
    Raises:
        HTTPException 401: if token missing, invalid, or expired
    
    Returns:
        CurrentUser context with claims
    """
    try:
        token = credentials.credentials
        
        # Decode and validate the access token
        claims = JWTService.verify_access_token(token, settings.jwt_secret_key)
        
        # Extract user_id from 'sub' claim
        user_id_str = claims.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        
        try:
            user_id = UUID(user_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        
        # Extract and validate tenant_id
        tenant_id_str = claims.get("tenant_id")
        if not tenant_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        
        try:
            tenant_id = UUID(tenant_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        
        # Extract roles
        roles = claims.get("roles", [])
        if not isinstance(roles, list):
            roles = [roles] if roles else []
        
        # Extract issued at and expiration times
        iat = claims.get("iat", 0)
        exp = claims.get("exp", 0)
        
        # Create and return CurrentUser instance
        return CurrentUser(
            user_id=user_id,
            tenant_id=tenant_id,
            roles=roles,
            iat=iat,
            exp=exp,
        )
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )


async def get_platform_admin_key(
    x_platform_admin_key: str = Header(None),
) -> str:
    """
    Validate platform admin key from header.
    
    Used for bootstrap endpoints that don't have users yet.
    
    Raises:
        HTTPException 401: if key missing or invalid
    """
    if not x_platform_admin_key or x_platform_admin_key != settings.platform_admin_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid platform admin key",
        )
    return x_platform_admin_key
