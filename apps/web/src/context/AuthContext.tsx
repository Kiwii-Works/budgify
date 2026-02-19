import React, { createContext, useContext, ReactNode, useState, useEffect } from 'react'
import { apiClient, setAccessToken, clearTokens } from '@/lib/api/client'

interface User {
  userId: string
  email: string
  username: string
  tenantId: string
  roles: string[]
  isActive: boolean
  createdAt: string
}

interface AuthContextType {
  // State
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  accessToken: string | null
  tenantId: string | null

  // Actions
  login: (email: string, password: string, tenantId: string) => Promise<void>
  logout: () => Promise<void>
  refreshToken: () => Promise<void>
  clearError: () => void
  hasRole: (role: string) => boolean
  hasAnyRole: (roles: string[]) => boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // State management
  const [user, setUser] = useState<User | null>(null)
  const [accessToken, setAccessTokenState] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Derived state
  const isAuthenticated = !!user && !!accessToken
  const tenantId = user?.tenantId || null

  // On mount: restore session from localStorage if available
  useEffect(() => {
    const restoredAccessToken = localStorage.getItem('accessToken')
    const restoredUser = localStorage.getItem('user')
    
    if (restoredAccessToken && restoredUser) {
      try {
        setAccessTokenState(restoredAccessToken)
        setAccessToken(restoredAccessToken)
        setUser(JSON.parse(restoredUser))
      } catch (err) {
        console.error('Failed to restore session:', err)
        clearTokens()
        localStorage.removeItem('accessToken')
        localStorage.removeItem('user')
      }
    }
  }, [])

  // Login action
  const login = async (email: string, password: string, tenantId: string) => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await apiClient.post<{ data: any }>('/api/auth/login', {
        email,
        password,
        tenant_id: tenantId,
      })

      const { access_token, refresh_token, user_id } = response.data.data

      // Store access token in memory and in API client
      setAccessTokenState(access_token)
      setAccessToken(access_token)

      // Store refresh token in localStorage (httpOnly cookie in production)
      localStorage.setItem('refreshToken', refresh_token)
      localStorage.setItem('accessToken', access_token)

      // Fetch and store user info
      const meResponse = await apiClient.get<{ data: User }>('/api/auth/me')
      const userData = meResponse.data.data
      
      setUser(userData)
      localStorage.setItem('user', JSON.stringify(userData))
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.error?.message || err.message || 'Login failed'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  // Logout action
  const logout = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const refreshToken = localStorage.getItem('refreshToken')
      if (refreshToken) {
        await apiClient.post('/api/auth/logout', {
          refresh_token: refreshToken,
        })
      }
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.error?.message || err.message || 'Logout failed'
      setError(errorMessage)
    } finally {
      // Clear state regardless of API result
      setAccessTokenState(null)
      setUser(null)
      clearTokens()
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')
      setIsLoading(false)
    }
  }

  // Refresh token action
  const refreshToken = async () => {
    const refresh_token = localStorage.getItem('refreshToken')
    if (!refresh_token) {
      await logout()
      return
    }

    try {
      const response = await apiClient.post<{ data: any }>('/api/auth/refresh', {
        refresh_token,
      })

      const { access_token, refresh_token: newRefreshToken } = response.data.data

      // Update tokens
      setAccessTokenState(access_token)
      setAccessToken(access_token)
      localStorage.setItem('accessToken', access_token)
      localStorage.setItem('refreshToken', newRefreshToken)
    } catch (err) {
      console.error('Token refresh failed:', err)
      await logout()
    }
  }

  // Helper methods
  const clearError = () => {
    setError(null)
  }

  const hasRole = (role: string) => {
    return user?.roles.includes(role) || false
  }

  const hasAnyRole = (roles: string[]) => {
    return user?.roles.some(r => roles.includes(r)) || false
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        isLoading,
        error,
        accessToken,
        tenantId,
        login,
        logout,
        refreshToken,
        clearError,
        hasRole,
        hasAnyRole,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
