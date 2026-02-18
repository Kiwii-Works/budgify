"""Quick test script for Phase 1B endpoints."""
import sys
from uuid import uuid4

# Add src to path
sys.path.insert(0, 'src')

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("=" * 60)
print("Testing Phase 1B Endpoints")
print("=" * 60)

# Test 1: Create Tenant
print("\n1. Testing POST /api/platform/tenants")
print("-" * 60)
response = client.post(
    "/api/platform/tenants",
    headers={"X-Platform-Admin-Key": "change-me"},
    json={
        "tenant_name": f"Test Tenant {uuid4().hex[:8]}",
        "initial_admin": {
            "username": f"admin_{uuid4().hex[:8]}",
            "first_name": "Admin",
            "last_name": "User",
            "email": f"admin_{uuid4().hex[:8]}@test.com",
            "phone_number": f"+1{uuid4().int % 10000000000:010d}",
            "password": "password123"
        }
    }
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 201:
    tenant_data = response.json()['data']
    tenant_id = tenant_data['tenant_id']
    admin_user_id = tenant_data['admin_user_id']
    print(f"[OK] Tenant created: {tenant_id}")
    print(f"[OK] Admin user created: {admin_user_id}")

    # Test 2: Register User
    print("\n2. Testing POST /api/auth/register")
    print("-" * 60)
    response = client.post(
        "/api/auth/register",
        headers={"X-Tenant-Id": tenant_id},
        json={
            "username": f"user_{uuid4().hex[:8]}",
            "first_name": "Test",
            "last_name": "User",
            "email": f"test_{uuid4().hex[:8]}@example.com",
            "phone_number": f"+1{uuid4().int % 10000000000:010d}",
            "password": "password123"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 201:
        user_data = response.json()['data']
        user_id = user_data['user_id']
        print(f"[OK] User registered: {user_id}")

        # Test 3: Update User
        print("\n3. Testing PATCH /api/admin/users/{user_id}")
        print("-" * 60)
        response = client.patch(
            f"/api/admin/users/{user_id}",
            headers={"X-User-Id": admin_user_id},
            json={
                "first_name": "Updated",
                "last_name": "Name"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 200:
            print(f"[OK] User updated successfully")
        else:
            print(f"[FAIL] Failed to update user")

        # Test 4: Toggle User Active
        print("\n4. Testing PATCH /api/admin/users/{user_id}/activate")
        print("-" * 60)
        response = client.patch(
            f"/api/admin/users/{user_id}/activate",
            headers={"X-User-Id": admin_user_id},
            json={"is_active": False}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 200:
            print(f"[OK] User deactivated successfully")
        else:
            print(f"[FAIL] Failed to toggle user active")
    else:
        print(f"[FAIL] Failed to register user")
else:
    print(f"[FAIL] Failed to create tenant")

print("\n" + "=" * 60)
print("Testing Complete")
print("=" * 60)
