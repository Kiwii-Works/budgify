"""Identity API routes."""

from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.response import create_success_response
from app.core.dependencies.auth import get_current_user, CurrentUser
from app.core.errors import (
    InvalidCredentialsError,
    UserInactiveError,
    TenantMembershipError,
    InvalidTokenError,
)
from app.modules.identity.application.auth_service import AuthService
from app.modules.identity.application.services import (
    CreateTenantService,
    RegisterUserService,
    ToggleUserActiveService,
    UpdateUserService,
)
from app.modules.identity.domain.exceptions import (
    ForbiddenError,
    InvalidPasswordError,
    RoleNotFoundError,
    TenantNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.modules.identity.domain.auth_schemas import (
    LoginRequest,
    RefreshTokenRequest,
    AuthResponse,
)
from app.modules.identity.infrastructure.repositories import (
    SQLAlchemyAuditRepository,
    SQLAlchemyMembershipRepository,
    SQLAlchemyRoleAssignmentRepository,
    SQLAlchemyRoleRepository,
    SQLAlchemyRefreshTokenRepository,
    SQLAlchemyTenantRepository,
    SQLAlchemyUserRepository,
)
from app.modules.identity.schemas import (
    AdminToggleActiveRequest,
    AdminUpdateUserRequest,
    CreateTenantRequest,
    CreateTenantResponse,
    RegisterRequest,
    RegisterResponse,
)

router = APIRouter(tags=["identity"])


# ===== Dependency Helpers =====


def verify_platform_key(x_platform_admin_key: str = Header(...)) -> None:
    """Verify platform admin key header."""
    if x_platform_admin_key != settings.platform_admin_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid platform admin key"
        )


def get_tenant_id(x_tenant_id: UUID = Header(...)) -> UUID:
    """Extract tenant ID from header."""
    return x_tenant_id


def get_current_user_id(x_user_id: UUID = Header(...)) -> UUID:
    """Extract current user ID from header (stub for Phase 1B)."""
    return x_user_id


# ===== Endpoints =====


@router.post("/platform/tenants", status_code=status.HTTP_201_CREATED)
async def create_tenant(
    request: CreateTenantRequest,
    db: Session = Depends(get_db),
    _: None = Depends(verify_platform_key),
):
    """Create tenant with optional admin user (platform admin only)."""
    transaction_uid = uuid4()

    try:
        # Instantiate repositories
        tenant_repo = SQLAlchemyTenantRepository(db)
        user_repo = SQLAlchemyUserRepository(db)
        role_repo = SQLAlchemyRoleRepository(db)
        membership_repo = SQLAlchemyMembershipRepository(db)
        role_assignment_repo = SQLAlchemyRoleAssignmentRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)

        # Instantiate service
        service = CreateTenantService(
            tenant_repo=tenant_repo,
            user_repo=user_repo,
            role_repo=role_repo,
            membership_repo=membership_repo,
            role_assignment_repo=role_assignment_repo,
            audit_repo=audit_repo,
        )

        # Execute
        initial_admin_dict = request.initial_admin.model_dump() if request.initial_admin else None
        tenant, admin_user = service.execute(
            tenant_name=request.tenant_name,
            initial_admin=initial_admin_dict,
            transaction_uid=transaction_uid,
        )

        # Commit
        db.commit()

        # Map to response
        response = CreateTenantResponse(
            tenant_id=str(tenant.tenant_id),
            tenant_name=tenant.tenant_name,
            admin_user_id=str(admin_user.user_id) if admin_user else None,
        )

        return create_success_response(data=response.model_dump())

    except UserAlreadyExistsError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except (RoleNotFoundError, InvalidPasswordError) as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    tenant_id: UUID = Depends(get_tenant_id),
    db: Session = Depends(get_db),
):
    """Register new user (requires X-Tenant-Id header)."""
    transaction_uid = uuid4()

    try:
        # Instantiate repositories
        user_repo = SQLAlchemyUserRepository(db)
        tenant_repo = SQLAlchemyTenantRepository(db)
        role_repo = SQLAlchemyRoleRepository(db)
        membership_repo = SQLAlchemyMembershipRepository(db)
        role_assignment_repo = SQLAlchemyRoleAssignmentRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)

        # Instantiate service
        service = RegisterUserService(
            user_repo=user_repo,
            tenant_repo=tenant_repo,
            role_repo=role_repo,
            membership_repo=membership_repo,
            role_assignment_repo=role_assignment_repo,
            audit_repo=audit_repo,
        )

        # Execute
        user = service.execute(
            tenant_id=tenant_id,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone_number=request.phone_number,
            password=request.password,
            transaction_uid=transaction_uid,
        )

        # Commit
        db.commit()

        # Map to response
        response = RegisterResponse(
            user_id=str(user.user_id),
            username=user.username,
            email=user.email,
        )

        return create_success_response(data=response.model_dump())

    except TenantNotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except UserAlreadyExistsError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except (InvalidPasswordError, RoleNotFoundError) as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.patch("/admin/users/{user_id}")
async def update_user(
    user_id: UUID,
    request: AdminUpdateUserRequest,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Update user (admin only, except password)."""
    transaction_uid = uuid4()

    try:
        # Instantiate repositories
        user_repo = SQLAlchemyUserRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)

        # Instantiate service
        service = UpdateUserService(
            user_repo=user_repo,
            audit_repo=audit_repo,
        )

        # Build updates dict (only include non-None fields)
        updates = {}
        if request.first_name is not None:
            updates["first_name"] = request.first_name
        if request.last_name is not None:
            updates["last_name"] = request.last_name
        if request.email is not None:
            updates["email"] = request.email
        if request.phone_number is not None:
            updates["phone_number"] = request.phone_number

        # Execute
        user = service.execute(
            user_id=user_id,
            updates=updates,
            modified_by=current_user_id,
            transaction_uid=transaction_uid,
        )

        # Commit
        db.commit()

        # Map to response
        response = {
            "user_id": str(user.user_id),
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "is_active": user.is_active,
        }

        return create_success_response(data=response)

    except UserNotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except UserAlreadyExistsError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ForbiddenError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e


@router.patch("/admin/users/{user_id}/activate")
async def toggle_active(
    user_id: UUID,
    request: AdminToggleActiveRequest,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Toggle user is_active (admin only)."""
    transaction_uid = uuid4()

    try:
        # Instantiate repositories
        user_repo = SQLAlchemyUserRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)

        # Instantiate service
        service = ToggleUserActiveService(
            user_repo=user_repo,
            audit_repo=audit_repo,
        )

        # Execute
        user = service.execute(
            user_id=user_id,
            is_active=request.is_active,
            modified_by=current_user_id,
            transaction_uid=transaction_uid,
        )

        # Commit
        db.commit()

        # Map to response
        response = {
            "user_id": str(user.user_id),
            "username": user.username,
            "is_active": user.is_active,
        }

        return create_success_response(data=response)

    except UserNotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForbiddenError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        ) from e

# ===== JWT Authentication Routes =====

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Resolve AuthService with repository dependencies."""
    user_repo = SQLAlchemyUserRepository(db)
    refresh_token_repo = SQLAlchemyRefreshTokenRepository(db)
    
    return AuthService(
        user_repository=user_repo,
        refresh_token_repository=refresh_token_repo,
    )


@router.post(
    "/auth/login",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    tags=["authentication"],
    summary="User login",
)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """
    Login endpoint.
    
    Authenticates user with email and password for specific tenant.
    Returns access token and refresh token.
    """
    try:
        auth_response = auth_service.login(
            email=request.email,
            password=request.password,
            tenant_id=request.tenant_id,
        )
        return create_success_response(auth_response)
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        ) from e
    except TenantMembershipError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this tenant",
        ) from e
    except UserInactiveError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User account is inactive",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e


@router.post(
    "/auth/refresh",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    tags=["authentication"],
    summary="Refresh access token",
)
async def refresh(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """
    Refresh token endpoint.
    
    Exchanges refresh token for new access token with rotation.
    Old refresh token is revoked.
    """
    try:
        auth_response = auth_service.refresh_token(
            refresh_token=request.refresh_token,
        )
        return create_success_response(auth_response)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e


@router.post(
    "/auth/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["authentication"],
    summary="User logout",
)
async def logout(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    """
    Logout endpoint.
    
    Revokes refresh token.
    """
    try:
        auth_service.logout(refresh_token=request.refresh_token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e


@router.get(
    "/auth/me",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    tags=["authentication"],
    summary="Get current user",
)
async def get_me(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """
    Get current user endpoint.
    
    Returns authenticated user information from JWT claims.
    Requires: Authorization: Bearer <access_token>
    """
    try:
        # Extract user_id from JWT
        user_id = current_user.user_id
        tenant_id = current_user.tenant_id
        roles = current_user.roles
        
        # Query fresh user data from DB
        user_repo = SQLAlchemyUserRepository(db)
        user = user_repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        response = {
            "user_id": str(user_id),
            "email": user.email,
            "username": user.username,
            "tenant_id": str(tenant_id),
            "roles": roles,
            "is_active": user.is_active,
            "created_at": user.created_date_utc.isoformat() if user.created_date_utc else None,
        }
        
        return create_success_response(response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e