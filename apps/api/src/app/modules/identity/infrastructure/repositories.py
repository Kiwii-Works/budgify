"""Concrete repository implementations for identity module."""

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.identity.domain.entities import (
    Role,
    Tenant,
    User,
    UserTenantMembership,
    UserTenantRole,
)
from app.modules.identity.domain.refresh_token import RefreshToken
from app.modules.identity.infrastructure.models import (
    OperationType,
)
from app.modules.identity.infrastructure.models import (
    Role as RoleModel,
)
from app.modules.identity.infrastructure.models import (
    Tenant as TenantModel,
)
from app.modules.identity.infrastructure.models import (
    TransactionLogDetails as TransactionLogDetailsModel,
)
from app.modules.identity.infrastructure.models import (
    TransactionsLog as TransactionsLogModel,
)
from app.modules.identity.infrastructure.models import (
    User as UserModel,
)
from app.modules.identity.infrastructure.models import (
    UserTenant as UserTenantModel,
)
from app.modules.identity.infrastructure.models import (
    UserTenantRole as UserTenantRoleModel,
)
from app.modules.identity.infrastructure.models import (
    UserRefreshToken as UserRefreshTokenModel,
)


class SQLAlchemyUserRepository:
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        """Create a new user."""
        # Convert domain entity to ORM model
        user_model = UserModel(
            user_id=user.user_id,
            username=user.username.lower(),  # Normalize
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email.lower(),  # Normalize
            phone_number=user.phone_number,
            password_hash=user.password_hash,
            is_active=user.is_active,
            is_platform_admin=user.is_platform_admin,
            created_by=user.created_by,
            modified_by=user.modified_by,
            created_date=user.created_date,
            created_date_utc=user.created_date_utc,
            modified_date=user.modified_date,
            modified_date_utc=user.modified_date_utc,
            operation_type=OperationType.ADDED,
            transaction_uid=getattr(user, "transaction_uid", None),
        )
        self.session.add(user_model)
        self.session.flush()
        return self._to_entity(user_model)

    def get_by_id(self, user_id: UUID) -> User | None:
        """Get user by ID."""
        user_model = self.session.query(UserModel).filter(UserModel.user_id == user_id).first()
        return self._to_entity(user_model) if user_model else None

    def get_by_email(self, email: str) -> User | None:
        """Get user by email (case-insensitive)."""
        user_model = self.session.query(UserModel).filter(UserModel.email == email.lower()).first()
        return self._to_entity(user_model) if user_model else None

    def get_by_username(self, username: str) -> User | None:
        """Get user by username (case-insensitive)."""
        user_model = (
            self.session.query(UserModel).filter(UserModel.username == username.lower()).first()
        )
        return self._to_entity(user_model) if user_model else None

    def get_by_phone(self, phone: str) -> User | None:
        """Get user by phone number."""
        user_model = self.session.query(UserModel).filter(UserModel.phone_number == phone).first()
        return self._to_entity(user_model) if user_model else None

    def update(self, user: User) -> User:
        """Update an existing user."""
        user_model = self.session.query(UserModel).filter(UserModel.user_id == user.user_id).first()
        if not user_model:
            raise ValueError(f"User {user.user_id} not found")

        # Update fields
        user_model.username = user.username.lower()
        user_model.first_name = user.first_name
        user_model.last_name = user.last_name
        user_model.email = user.email.lower()
        user_model.phone_number = user.phone_number
        user_model.is_active = user.is_active
        user_model.is_platform_admin = user.is_platform_admin
        user_model.modified_by = user.modified_by
        user_model.modified_date = user.modified_date
        user_model.modified_date_utc = user.modified_date_utc
        user_model.operation_type = OperationType.MODIFIED
        user_model.transaction_uid = getattr(user, "transaction_uid", None)

        self.session.flush()
        return self._to_entity(user_model)

    def _to_entity(self, model: UserModel) -> User:
        """Convert ORM model to domain entity."""
        return User(
            user_id=model.user_id,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            phone_number=model.phone_number,
            password_hash=model.password_hash,
            is_active=model.is_active,
            is_platform_admin=model.is_platform_admin,
            created_by=model.created_by,
            modified_by=model.modified_by,
            created_date=model.created_date,
            created_date_utc=model.created_date_utc,
            modified_date=model.modified_date,
            modified_date_utc=model.modified_date_utc,
        )

    def has_tenant_membership(self, user_id: UUID, tenant_id: UUID) -> bool:
        """Check if user has membership in tenant."""
        return (
            self.session.query(UserTenantModel)
            .filter(
                UserTenantModel.user_id == user_id,
                UserTenantModel.tenant_id == tenant_id,
            )
            .count()
            > 0
        )

    def get_user_roles_for_tenant(self, user_id: UUID, tenant_id: UUID) -> list[Role]:
        """Get all roles assigned to user in a specific tenant."""
        role_models = (
            self.session.query(RoleModel)
            .join(
                UserTenantRoleModel,
                RoleModel.role_id == UserTenantRoleModel.role_id,
            )
            .filter(
                UserTenantRoleModel.user_id == user_id,
                UserTenantRoleModel.tenant_id == tenant_id,
            )
            .all()
        )
        return [self._role_to_entity(r) for r in role_models]

    def _role_to_entity(self, model: RoleModel) -> Role:
        """Convert ORM Role model to domain entity."""
        return Role(
            role_id=model.role_id,
            role_name=model.role_name,
            created_by=model.created_by,
            modified_by=model.modified_by,
            created_date=model.created_date,
            created_date_utc=model.created_date_utc,
            modified_date=model.modified_date,
            modified_date_utc=model.modified_date_utc,
        )


class SQLAlchemyTenantRepository:
    """SQLAlchemy implementation of TenantRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, tenant: Tenant) -> Tenant:
        """Create a new tenant."""
        tenant_model = TenantModel(
            tenant_id=tenant.tenant_id,
            tenant_name=tenant.tenant_name,
            is_active=tenant.is_active,
            created_by=tenant.created_by,
            modified_by=tenant.modified_by,
            created_date=tenant.created_date,
            created_date_utc=tenant.created_date_utc,
            modified_date=tenant.modified_date,
            modified_date_utc=tenant.modified_date_utc,
            operation_type=OperationType.ADDED,
            transaction_uid=getattr(tenant, "transaction_uid", None),
        )
        self.session.add(tenant_model)
        self.session.flush()
        return self._to_entity(tenant_model)

    def get_by_id(self, tenant_id: UUID) -> Tenant | None:
        """Get tenant by ID."""
        tenant_model = (
            self.session.query(TenantModel).filter(TenantModel.tenant_id == tenant_id).first()
        )
        return self._to_entity(tenant_model) if tenant_model else None

    def exists(self, tenant_id: UUID) -> bool:
        """Check if tenant exists."""
        return (
            self.session.query(TenantModel).filter(TenantModel.tenant_id == tenant_id).count() > 0
        )

    def _to_entity(self, model: TenantModel) -> Tenant:
        """Convert ORM model to domain entity."""
        return Tenant(
            tenant_id=model.tenant_id,
            tenant_name=model.tenant_name,
            is_active=model.is_active,
            created_by=model.created_by,
            modified_by=model.modified_by,
            created_date=model.created_date,
            created_date_utc=model.created_date_utc,
            modified_date=model.modified_date,
            modified_date_utc=model.modified_date_utc,
        )


class SQLAlchemyRoleRepository:
    """SQLAlchemy implementation of RoleRepository."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, role_name: str) -> Role | None:
        """Get role by name."""
        role_model = self.session.query(RoleModel).filter(RoleModel.role_name == role_name).first()
        return self._to_entity(role_model) if role_model else None

    def _to_entity(self, model: RoleModel) -> Role:
        """Convert ORM model to domain entity."""
        return Role(
            role_id=model.role_id,
            role_name=model.role_name,
            created_by=model.created_by,
            modified_by=model.modified_by,
            created_date=model.created_date,
            created_date_utc=model.created_date_utc,
            modified_date=model.modified_date,
            modified_date_utc=model.modified_date_utc,
        )


class SQLAlchemyMembershipRepository:
    """SQLAlchemy implementation of MembershipRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, membership: UserTenantMembership) -> UserTenantMembership:
        """Create a new user-tenant membership."""
        membership_model = UserTenantModel(
            user_id=membership.user_id,
            tenant_id=membership.tenant_id,
            is_default=membership.is_default,
            created_by=membership.created_by,
            modified_by=membership.modified_by,
            created_date=membership.created_date,
            created_date_utc=membership.created_date_utc,
            modified_date=membership.modified_date,
            modified_date_utc=membership.modified_date_utc,
            operation_type=OperationType.ADDED,
            transaction_uid=getattr(membership, "transaction_uid", None),
        )
        self.session.add(membership_model)
        self.session.flush()
        return self._to_entity(membership_model)

    def _to_entity(self, model: UserTenantModel) -> UserTenantMembership:
        """Convert ORM model to domain entity."""
        return UserTenantMembership(
            user_id=model.user_id,
            tenant_id=model.tenant_id,
            is_default=model.is_default,
            created_by=model.created_by,
            modified_by=model.modified_by,
            created_date=model.created_date,
            created_date_utc=model.created_date_utc,
            modified_date=model.modified_date,
            modified_date_utc=model.modified_date_utc,
        )


class SQLAlchemyRoleAssignmentRepository:
    """SQLAlchemy implementation of RoleAssignmentRepository."""

    def __init__(self, session: Session):
        self.session = session

    def assign(self, assignment: UserTenantRole) -> UserTenantRole:
        """Assign a role to a user in a tenant."""
        assignment_model = UserTenantRoleModel(
            user_id=assignment.user_id,
            tenant_id=assignment.tenant_id,
            role_id=assignment.role_id,
            created_by=assignment.created_by,
            modified_by=assignment.modified_by,
            created_date=assignment.created_date,
            created_date_utc=assignment.created_date_utc,
            modified_date=assignment.modified_date,
            modified_date_utc=assignment.modified_date_utc,
            operation_type=OperationType.ADDED,
            transaction_uid=getattr(assignment, "transaction_uid", None),
        )
        self.session.add(assignment_model)
        self.session.flush()
        return self._to_entity(assignment_model)

    def _to_entity(self, model: UserTenantRoleModel) -> UserTenantRole:
        """Convert ORM model to domain entity."""
        return UserTenantRole(
            user_id=model.user_id,
            tenant_id=model.tenant_id,
            role_id=model.role_id,
            created_by=model.created_by,
            modified_by=model.modified_by,
            created_date=model.created_date,
            created_date_utc=model.created_date_utc,
            modified_date=model.modified_date,
            modified_date_utc=model.modified_date_utc,
        )


class SQLAlchemyAuditRepository:
    """SQLAlchemy implementation of AuditRepository."""

    def __init__(self, session: Session):
        self.session = session

    def log_transaction(
        self,
        transaction_uid: UUID,
        action_type: str,
        user_id: UUID | None,
        tenant_id: UUID | None,
    ) -> None:
        """Log a transaction to transactions_log."""
        now = datetime.now(UTC)
        transaction = TransactionsLogModel(
            transaction_uid=transaction_uid,
            action_type=action_type,
            transaction_date=now.replace(tzinfo=None),
            transaction_date_utc=now,
            modified_by=user_id,
            tenant_id=tenant_id,
        )
        self.session.add(transaction)
        self.session.flush()

    def log_detail(
        self,
        transaction_uid: UUID,
        action_type: str,
        entity_domain: str,
        entity_id: UUID,
        operation_type: str,
        tenant_id: UUID | None,
    ) -> None:
        """Log transaction details to transaction_log_details."""
        detail = TransactionLogDetailsModel(
            transaction_uid=transaction_uid,
            action_type=action_type,
            entity_domain=entity_domain,
            entity_id=entity_id,
            transaction_description=OperationType[operation_type],
            changes=None,  # Optional for Phase 1B
            tenant_id=tenant_id,
        )
        self.session.add(detail)
        self.session.flush()

class SQLAlchemyRefreshTokenRepository:
    """SQLAlchemy implementation of RefreshTokenRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, refresh_token: RefreshToken) -> RefreshToken:
        """Create a new refresh token record."""
        token_model = UserRefreshTokenModel(
            refresh_token_id=refresh_token.refresh_token_id,
            user_id=refresh_token.user_id,
            tenant_id=refresh_token.tenant_id,
            token_hash=refresh_token.token_hash,
            expires_at=refresh_token.expires_at,
            revoked_at=refresh_token.revoked_at,
            created_at=refresh_token.created_at,
            last_used_at=refresh_token.last_used_at,
            created_by=refresh_token.created_by,
        )
        self.session.add(token_model)
        self.session.flush()
        return self._to_entity(token_model)

    def get_by_token_hash(
        self,
        token_hash: str,
        tenant_id: UUID | None = None,
    ) -> RefreshToken | None:
        """Get refresh token by its hash."""
        query = self.session.query(UserRefreshTokenModel).filter(
            UserRefreshTokenModel.token_hash == token_hash
        )
        if tenant_id:
            query = query.filter(UserRefreshTokenModel.tenant_id == tenant_id)
        
        token_model = query.first()
        return self._to_entity(token_model) if token_model else None

    def revoke(
        self,
        refresh_token_id: UUID,
        tenant_id: UUID,
    ) -> None:
        """Revoke a refresh token by setting revoked_at."""
        token_model = self.session.query(UserRefreshTokenModel).filter(
            UserRefreshTokenModel.refresh_token_id == refresh_token_id,
            UserRefreshTokenModel.tenant_id == tenant_id,
        ).first()
        
        if token_model:
            token_model.revoked_at = datetime.now(UTC)
            self.session.flush()

    def delete_expired(self) -> int:
        """Delete expired refresh tokens (older than expiry date)."""
        now = datetime.now(UTC)
        result = self.session.query(UserRefreshTokenModel).filter(
            UserRefreshTokenModel.expires_at <= now
        ).delete()
        self.session.flush()
        return result

    def _to_entity(self, model: UserRefreshTokenModel) -> RefreshToken:
        """Convert ORM model to domain entity."""
        return RefreshToken(
            refresh_token_id=model.refresh_token_id,
            user_id=model.user_id,
            tenant_id=model.tenant_id,
            token_hash=model.token_hash,
            expires_at=model.expires_at,
            revoked_at=model.revoked_at,
            created_at=model.created_at,
            last_used_at=model.last_used_at,
            created_by=model.created_by,
        )