// API Response Types
export interface ApiMeta {
  request_id: string
  timestamp: string
  pagination?: {
    page: number
    page_size: number
    total: number
  }
}

export interface ApiSuccessResponse<T> {
  data: T
  meta: ApiMeta
}

export interface ApiErrorDetail {
  field?: string
  issue?: string
}

export interface ApiErrorResponse {
  error: {
    code: string
    message: string
    details?: ApiErrorDetail[]
  }
  meta: ApiMeta
}

// Health
export interface HealthResponse {
  status: string
}

// Auth
export interface LoginRequest {
  email: string
  password: string
  tenant_id: string
}

export interface AuthTokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user_id: string
  tenant_id: string
}

export interface RefreshTokenRequest {
  refresh_token: string
}

export interface LogoutRequest {
  refresh_token: string
}

// Tenant
export interface CreateTenantRequest {
  tenant_name: string
  initial_admin?: {
    username: string
    first_name: string
    last_name: string
    email: string
    password: string
    phone_number?: string
  }
}

export interface CreateTenantResponse {
  tenant_id: string
  tenant_name: string
  admin_user_id?: string
}

// User
export interface RegisterRequest {
  username: string
  first_name: string
  last_name: string
  email: string
  phone_number?: string
  password: string
}

export interface RegisterResponse {
  user_id: string
  username: string
  email: string
}

export interface User {
  user_id: string
  username: string
  first_name: string
  last_name: string
  email: string
  phone_number?: string
  is_active: boolean
}

export interface AdminUpdateUserRequest {
  first_name?: string
  last_name?: string
  email?: string
  phone_number?: string
}

export interface AdminToggleActiveRequest {
  is_active: boolean
}

// Session context
export interface SessionContextType {
  tenantId: string | null
  userId: string | null
  platformAdminKey: string | null
  setTenantId: (id: string | null) => void
  setUserId: (id: string | null) => void
  setPlatformAdminKey: (key: string | null) => void
  clearSession: () => void
}

// ===== FINANCE TYPES =====

// Account Categories
export interface AccountCategory {
  category_id: string
  tenant_id: string
  name: string
  description?: string
  is_active: boolean
}

export interface CreateAccountCategoryRequest {
  name: string
  description?: string
}

export interface UpdateAccountCategoryRequest {
  name?: string
  description?: string
  is_active?: boolean
}

// Accounts
export interface Account {
  account_id: string
  tenant_id: string
  category_id: string
  name: string
  description?: string
  type: 'INCOME' | 'EXPENSE'
  is_active: boolean
}

export interface CreateAccountRequest {
  category_id: string
  name: string
  description?: string
  type: 'INCOME' | 'EXPENSE'
}

export interface UpdateAccountRequest {
  category_id?: string
  name?: string
  description?: string
  type?: 'INCOME' | 'EXPENSE'
  is_active?: boolean
}

// Transactions
export interface Transaction {
  transaction_id: string
  tenant_id: string
  account_id: string
  amount: number
  currency: string
  occurred_on: string
  notes?: string
  direction: 'INCOME' | 'EXPENSE'
  created_by: string
  created_date: string
  modified_by?: string
  modified_date?: string
}

export interface CreateTransactionRequest {
  account_id: string
  amount: number
  currency?: string
  occurred_on: string
  notes?: string
}

export interface UpdateTransactionRequest {
  account_id?: string
  amount?: number
  currency?: string
  occurred_on?: string
  notes?: string
}

// Pagination for Finance endpoints
export interface FinancePaginationParams {
  page?: number
  page_size?: number
}
