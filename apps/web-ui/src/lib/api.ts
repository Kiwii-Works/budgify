import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios'
import { ApiErrorResponse } from '../types'

// Base URL for API - use Vite environment variable or default to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance with base configuration
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - automatically add session headers to every request
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Retrieve session data from localStorage
    const tenantId = localStorage.getItem('tenantId')
    const userId = localStorage.getItem('userId')
    const platformAdminKey = localStorage.getItem('platformAdminKey')
    const accessToken = localStorage.getItem('accessToken')

    if (tenantId) {
      config.headers['X-Tenant-Id'] = tenantId
    }

    if (userId) {
      config.headers['X-User-Id'] = userId
    }

    if (platformAdminKey) {
      config.headers['X-Platform-Admin-Key'] = platformAdminKey
    }

    if (accessToken) {
      config.headers['Authorization'] = `Bearer ${accessToken}`
    }

    // Add request ID
    config.headers['X-Request-Id'] = generateRequestId()

    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ApiErrorResponse>) => {
    if (error.response?.status === 401) {
      // Try to refresh token
      const refreshToken = localStorage.getItem('refreshToken')
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {
            refresh_token: refreshToken,
          })
          const { access_token } = response.data.data
          localStorage.setItem('accessToken', access_token)

          // Retry original request
          if (error.config) {
            error.config.headers['Authorization'] = `Bearer ${access_token}`
            return apiClient(error.config)
          }
        } catch (refreshError) {
          // Clear session and redirect to login
          localStorage.clear()
          window.location.href = '/login'
          return Promise.reject(refreshError)
        }
      } else {
        localStorage.clear()
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

function generateRequestId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

export default apiClient
