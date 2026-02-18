import React, { createContext, useContext, ReactNode, useState, useEffect } from 'react'
import { SessionContextType } from '../types'

// Context for managing user session state
const SessionContext = createContext<SessionContextType | undefined>(undefined)

// Session provider component - wraps app and manages session state
export const SessionProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [tenantId, setTenantIdState] = useState<string | null>(null)
  const [userId, setUserIdState] = useState<string | null>(null)
  const [platformAdminKey, setPlatformAdminKeyState] = useState<string | null>(null)

  // Load session data from localStorage on component mount
  useEffect(() => {
    const savedTenantId = localStorage.getItem('tenantId')
    const savedUserId = localStorage.getItem('userId')
    const savedPlatformAdminKey = localStorage.getItem('platformAdminKey')

    if (savedTenantId) setTenantIdState(savedTenantId)
    if (savedUserId) setUserIdState(savedUserId)
    if (savedPlatformAdminKey) setPlatformAdminKeyState(savedPlatformAdminKey)
  }, [])

  // Set tenant ID and persist to localStorage
  const setTenantId = (id: string | null) => {
    setTenantIdState(id)
    if (id) {
      localStorage.setItem('tenantId', id)
    } else {
      localStorage.removeItem('tenantId')
    }
  }

  // Set user ID and persist to localStorage
  const setUserId = (id: string | null) => {
    setUserIdState(id)
    if (id) {
      localStorage.setItem('userId', id)
    } else {
      localStorage.removeItem('userId')
    }
  }

  // Set platform admin key and persist to localStorage
  const setPlatformAdminKey = (key: string | null) => {
    setPlatformAdminKeyState(key)
    if (key) {
      localStorage.setItem('platformAdminKey', key)
    } else {
      localStorage.removeItem('platformAdminKey')
    }
  }

  // Clear all session data
  const clearSession = () => {
    setTenantIdState(null)
    setUserIdState(null)
    setPlatformAdminKeyState(null)
    localStorage.removeItem('tenantId')
    localStorage.removeItem('userId')
    localStorage.removeItem('platformAdminKey')
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  return (
    <SessionContext.Provider
      value={{
        tenantId,
        userId,
        platformAdminKey,
        setTenantId,
        setUserId,
        setPlatformAdminKey,
        clearSession,
      }}
    >
      {children}
    </SessionContext.Provider>
  )
}

export const useSession = () => {
  const context = useContext(SessionContext)
  if (!context) {
    throw new Error('useSession must be used within a SessionProvider')
  }
  return context
}
