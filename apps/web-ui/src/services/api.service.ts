import { apiClient } from '../lib/api'
import {
  AuthTokenResponse,
  CreateTenantRequest,
  CreateTenantResponse,
  HealthResponse,
  RegisterRequest,
  RegisterResponse,
  ApiSuccessResponse,
  User,
  AdminUpdateUserRequest,
  AdminToggleActiveRequest,
} from '../types'

// API service for health checks
export const healthService = {
  check: async (): Promise<HealthResponse> => {
    const response = await apiClient.get<ApiSuccessResponse<HealthResponse>>('/api/health')
    return response.data.data
  },
}

// API service for authentication
export const authService = {
  login: async (email: string, password: string): Promise<AuthTokenResponse> => {
    const response = await apiClient.post<ApiSuccessResponse<AuthTokenResponse>>('/api/auth/login', {
      email,
      password,
    })
    return response.data.data
  },

  refresh: async (refreshToken: string): Promise<AuthTokenResponse> => {
    const response = await apiClient.post<ApiSuccessResponse<AuthTokenResponse>>('/api/auth/refresh', {
      refresh_token: refreshToken,
    })
    return response.data.data
  },

  logout: async (refreshToken: string): Promise<void> => {
    await apiClient.post('/api/auth/logout', {
      refresh_token: refreshToken,
    })
  },
}

// API service for tenant management
export const tenantService = {
  create: async (request: CreateTenantRequest, platformAdminKey: string): Promise<CreateTenantResponse> => {
    const response = await apiClient.post<ApiSuccessResponse<CreateTenantResponse>>(
      '/api/platform/tenants',
      request,
      {
        headers: {
          'X-Platform-Admin-Key': platformAdminKey,
        },
      }
    )
    return response.data.data
  },
}

// API service for user management
export const userService = {
  register: async (request: RegisterRequest, tenantId: string): Promise<RegisterResponse> => {
    const response = await apiClient.post<ApiSuccessResponse<RegisterResponse>>(
      '/api/auth/register',
      request,
      {
        headers: {
          'X-Tenant-Id': tenantId,
        },
      }
    )
    return response.data.data
  },

  update: async (userId: string, request: AdminUpdateUserRequest, currentUserId: string): Promise<User> => {
    const response = await apiClient.patch<ApiSuccessResponse<User>>(
      `/api/admin/users/${userId}`,
      request,
      {
        headers: {
          'X-User-Id': currentUserId,
        },
      }
    )
    return response.data.data
  },

  toggleActive: async (userId: string, isActive: boolean, currentUserId: string): Promise<User> => {
    const response = await apiClient.patch<ApiSuccessResponse<User>>(
      `/api/admin/users/${userId}/activate`,
      { is_active: isActive },
      {
        headers: {
          'X-User-Id': currentUserId,
        },
      }
    )
    return response.data.data
  },
}
