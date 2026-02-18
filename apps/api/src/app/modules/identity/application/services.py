"""Application services for identity module."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from passlib.context import CryptContext

from app.modules.identity.domain.entities import Tenant, User, UserTenantMembership, UserTenantRole
from app.modules.identity.domain.exceptions import (
    InvalidPasswordError,
    RoleNotFoundError,
    TenantNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.modules.identity.domain.interfaces import (
    AuditRepository,
    MembershipRepository,
    RoleAssignmentRepository,
    RoleRepository,
    TenantRepository,
    UserRepository,
)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_and_hash_password(password: str) -> str:
    """
    Validate and hash password.

    Bcrypt has a maximum password length of 72 bytes.
    """
    # Check minimum length
    if len(password) < 8:
        raise InvalidPasswordError("Password must be at least 8 characters")

    # Check maximum length (72 bytes for bcrypt)
    # Encode to UTF-8 to check byte length
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        raise InvalidPasswordError("Password is too long (maximum 72 bytes)")

    # Hash the password
    return pwd_context.hash(password)


class RegisterUserService:
    """Service for registering a new user."""

    def __init__(
        self,
        user_repo: UserRepository,
        tenant_repo: TenantRepository,
        role_repo: RoleRepository,
        membership_repo: MembershipRepository,
        role_assignment_repo: RoleAssignmentRepository,
        audit_repo: AuditRepository,
    ):
        self.user_repo = user_repo
        self.tenant_repo = tenant_repo
        self.role_repo = role_repo
        self.membership_repo = membership_repo
        self.role_assignment_repo = role_assignment_repo
        self.audit_repo = audit_repo

    def execute(
        self,
        tenant_id: UUID,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        password: str,
        transaction_uid: UUID,
    ) -> User:
        """
        Register a new user.

        Steps:
        1. Check tenant exists
        2. Validate password
        3. Check username/email/phone not taken
        4. Hash password
        5. Create user
        6. Create membership
        7. Assign READER role
        8. Log audit trail
        """
        # 1. Check tenant exists
        if not self.tenant_repo.exists(tenant_id):
            raise TenantNotFoundError(f"Tenant {tenant_id} does not exist")

        # 2. Check username/email/phone not taken
        if self.user_repo.get_by_username(username):
            raise UserAlreadyExistsError("username", username)
        if self.user_repo.get_by_email(email):
            raise UserAlreadyExistsError("email", email)
        if self.user_repo.get_by_phone(phone_number):
            raise UserAlreadyExistsError("phone_number", phone_number)

        # 3. Validate and hash password
        password_hash = validate_and_hash_password(password)

        # 5. Create user
        now = datetime.now(UTC)
        user_id = uuid4()
        user = User(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password_hash=password_hash,
            is_active=True,
            is_platform_admin=False,
            created_by=None,  # Self-registration
            modified_by=None,
            created_date=now.replace(tzinfo=None),
            created_date_utc=now,
            modified_date=None,
            modified_date_utc=None,
        )
        # Attach transaction_uid for repository
        user.transaction_uid = transaction_uid
        user = self.user_repo.create(user)

        # 6. Create membership
        membership = UserTenantMembership(
            user_id=user_id,
            tenant_id=tenant_id,
            is_default=True,
            created_by=None,
            modified_by=None,
            created_date=now.replace(tzinfo=None),
            created_date_utc=now,
            modified_date=None,
            modified_date_utc=None,
        )
        membership.transaction_uid = transaction_uid
        self.membership_repo.create(membership)

        # 7. Assign READER role
        reader_role = self.role_repo.get_by_name("READER")
        if not reader_role:
            raise RoleNotFoundError("READER role not found")

        assignment = UserTenantRole(
            user_id=user_id,
            tenant_id=tenant_id,
            role_id=reader_role.role_id,
            created_by=None,
            modified_by=None,
            created_date=now.replace(tzinfo=None),
            created_date_utc=now,
            modified_date=None,
            modified_date_utc=None,
        )
        assignment.transaction_uid = transaction_uid
        self.role_assignment_repo.assign(assignment)

        # 8. Log audit trail
        self.audit_repo.log_transaction(
            transaction_uid=transaction_uid,
            action_type="Register",
            user_id=None,  # Self-registration
            tenant_id=tenant_id,
        )
        self.audit_repo.log_detail(
            transaction_uid=transaction_uid,
            action_type="Register",
            entity_domain="users",
            entity_id=user_id,
            operation_type="ADDED",
            tenant_id=tenant_id,
        )

        return user


class CreateTenantService:
    """Service for creating a new tenant with optional admin."""

    def __init__(
        self,
        tenant_repo: TenantRepository,
        user_repo: UserRepository,
        role_repo: RoleRepository,
        membership_repo: MembershipRepository,
        role_assignment_repo: RoleAssignmentRepository,
        audit_repo: AuditRepository,
    ):
        self.tenant_repo = tenant_repo
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.membership_repo = membership_repo
        self.role_assignment_repo = role_assignment_repo
        self.audit_repo = audit_repo

    def execute(
        self,
        tenant_name: str,
        initial_admin: dict | None,
        transaction_uid: UUID,
    ) -> tuple[Tenant, User | None]:
        """
        Create a new tenant with optional admin user.

        Steps:
        1. Create tenant
        2. If initial_admin provided:
           a. Hash password
           b. Create user (is_platform_admin=False)
           c. Create membership
           d. Assign SUDO role
        3. Log audit trail
        """
        now = datetime.now(UTC)
        tenant_id = uuid4()

        # 1. Create tenant
        tenant = Tenant(
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            is_active=True,
            created_by=None,
            modified_by=None,
            created_date=now.replace(tzinfo=None),
            created_date_utc=now,
            modified_date=None,
            modified_date_utc=None,
        )
        tenant.transaction_uid = transaction_uid
        tenant = self.tenant_repo.create(tenant)

        admin_user = None

        # 2. If initial_admin provided
        if initial_admin:
            # Check for duplicates
            if self.user_repo.get_by_username(initial_admin["username"]):
                raise UserAlreadyExistsError("username", initial_admin["username"])
            if self.user_repo.get_by_email(initial_admin["email"]):
                raise UserAlreadyExistsError("email", initial_admin["email"])
            if self.user_repo.get_by_phone(initial_admin["phone_number"]):
                raise UserAlreadyExistsError("phone_number", initial_admin["phone_number"])

            # Validate and hash password
            password_hash = validate_and_hash_password(initial_admin["password"])

            # Create user
            user_id = uuid4()
            admin_user = User(
                user_id=user_id,
                username=initial_admin["username"],
                first_name=initial_admin["first_name"],
                last_name=initial_admin["last_name"],
                email=initial_admin["email"],
                phone_number=initial_admin["phone_number"],
                password_hash=password_hash,
                is_active=True,
                is_platform_admin=False,
                created_by=None,
                modified_by=None,
                created_date=now.replace(tzinfo=None),
                created_date_utc=now,
                modified_date=None,
                modified_date_utc=None,
            )
            admin_user.transaction_uid = transaction_uid
            admin_user = self.user_repo.create(admin_user)

            # Create membership
            membership = UserTenantMembership(
                user_id=user_id,
                tenant_id=tenant_id,
                is_default=True,
                created_by=None,
                modified_by=None,
                created_date=now.replace(tzinfo=None),
                created_date_utc=now,
                modified_date=None,
                modified_date_utc=None,
            )
            membership.transaction_uid = transaction_uid
            self.membership_repo.create(membership)

            # Assign SUDO role
            sudo_role = self.role_repo.get_by_name("SUDO")
            if not sudo_role:
                raise RoleNotFoundError("SUDO role not found")

            assignment = UserTenantRole(
                user_id=user_id,
                tenant_id=tenant_id,
                role_id=sudo_role.role_id,
                created_by=None,
                modified_by=None,
                created_date=now.replace(tzinfo=None),
                created_date_utc=now,
                modified_date=None,
                modified_date_utc=None,
            )
            assignment.transaction_uid = transaction_uid
            self.role_assignment_repo.assign(assignment)

        # 3. Log audit trail
        self.audit_repo.log_transaction(
            transaction_uid=transaction_uid,
            action_type="CreateTenant",
            user_id=None,
            tenant_id=tenant_id,
        )
        self.audit_repo.log_detail(
            transaction_uid=transaction_uid,
            action_type="CreateTenant",
            entity_domain="tenants",
            entity_id=tenant_id,
            operation_type="ADDED",
            tenant_id=tenant_id,
        )

        if admin_user:
            self.audit_repo.log_detail(
                transaction_uid=transaction_uid,
                action_type="CreateTenant",
                entity_domain="users",
                entity_id=admin_user.user_id,
                operation_type="ADDED",
                tenant_id=tenant_id,
            )

        return tenant, admin_user


class UpdateUserService:
    """Service for updating user profile (admin)."""

    def __init__(
        self,
        user_repo: UserRepository,
        audit_repo: AuditRepository,
    ):
        self.user_repo = user_repo
        self.audit_repo = audit_repo

    def execute(
        self,
        user_id: UUID,
        updates: dict,
        modified_by: UUID,
        transaction_uid: UUID,
    ) -> User:
        """
        Update user profile (admin).

        Allowed updates: first_name, last_name, email, phone_number
        NOT allowed: password (use separate endpoint)
        """
        # 1. Get user
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")

        # 2. Validate updates
        if "email" in updates:
            existing = self.user_repo.get_by_email(updates["email"])
            if existing and existing.user_id != user_id:
                raise UserAlreadyExistsError("email", updates["email"])

        if "phone_number" in updates:
            existing = self.user_repo.get_by_phone(updates["phone_number"])
            if existing and existing.user_id != user_id:
                raise UserAlreadyExistsError("phone_number", updates["phone_number"])

        # 3. Apply updates
        now = datetime.now(UTC)
        if "first_name" in updates:
            user.first_name = updates["first_name"]
        if "last_name" in updates:
            user.last_name = updates["last_name"]
        if "email" in updates:
            user.email = updates["email"]
        if "phone_number" in updates:
            user.phone_number = updates["phone_number"]

        # 4. Set audit fields
        user.modified_by = modified_by
        user.modified_date = now.replace(tzinfo=None)
        user.modified_date_utc = now
        user.transaction_uid = transaction_uid

        # 5. Save
        user = self.user_repo.update(user)

        # 6. Log audit trail
        self.audit_repo.log_transaction(
            transaction_uid=transaction_uid,
            action_type="UpdateUser",
            user_id=modified_by,
            tenant_id=None,
        )
        self.audit_repo.log_detail(
            transaction_uid=transaction_uid,
            action_type="UpdateUser",
            entity_domain="users",
            entity_id=user_id,
            operation_type="MODIFIED",
            tenant_id=None,
        )

        return user


class ToggleUserActiveService:
    """Service for toggling user is_active status (admin)."""

    def __init__(
        self,
        user_repo: UserRepository,
        audit_repo: AuditRepository,
    ):
        self.user_repo = user_repo
        self.audit_repo = audit_repo

    def execute(
        self,
        user_id: UUID,
        is_active: bool,
        modified_by: UUID,
        transaction_uid: UUID,
    ) -> User:
        """Toggle user is_active status."""
        # 1. Get user
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")

        # 2. Update is_active
        now = datetime.now(UTC)
        user.is_active = is_active
        user.modified_by = modified_by
        user.modified_date = now.replace(tzinfo=None)
        user.modified_date_utc = now
        user.transaction_uid = transaction_uid

        # 3. Save
        user = self.user_repo.update(user)

        # 4. Log audit trail
        self.audit_repo.log_transaction(
            transaction_uid=transaction_uid,
            action_type="ToggleUserActive",
            user_id=modified_by,
            tenant_id=None,
        )
        self.audit_repo.log_detail(
            transaction_uid=transaction_uid,
            action_type="ToggleUserActive",
            entity_domain="users",
            entity_id=user_id,
            operation_type="MODIFIED",
            tenant_id=None,
        )

        return user
