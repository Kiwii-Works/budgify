"""Identity API routes."""

from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.response import create_success_response
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
from app.modules.identity.infrastructure.repositories import (
    SQLAlchemyAuditRepository,
    SQLAlchemyMembershipRepository,
    SQLAlchemyRoleAssignmentRepository,
    SQLAlchemyRoleRepository,
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
