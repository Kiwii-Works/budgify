/**
 * API request/response types matching the Phase 1B backend.
 */

export interface ApiResponse<T = unknown> {
  data: T;
  meta: {
    request_id: string;
    timestamp: string;
  };
}

export interface ApiError {
  detail: string;
}

// Register endpoint types
export interface RegisterRequest {
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string;
  password: string;
}

export interface RegisterResponse {
  user_id: string;
  username: string;
  email: string;
}

// Create tenant endpoint types (for dev/testing)
export interface CreateTenantRequest {
  tenant_name: string;
  initial_admin?: {
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    phone_number: string;
    password: string;
  };
}

export interface CreateTenantResponse {
  tenant_id: string;
  tenant_name: string;
  admin_user_id: string | null;
}
