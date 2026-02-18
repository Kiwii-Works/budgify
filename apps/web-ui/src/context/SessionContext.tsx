import React, { createContext, useContext, ReactNode, useState, useEffect } from 'react'
import { SessionContextType } from '../types'

const SessionContext = createContext<SessionContextType | undefined>(undefined)

export const SessionProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [tenantId, setTenantIdState] = useState<string | null>(null)
  const [userId, setUserIdState] = useState<string | null>(null)
  const [platformAdminKey, setPlatformAdminKeyState] = useState<string | null>(null)

  // Load from localStorage on mount
  useEffect(() => {
    const savedTenantId = localStorage.getItem('tenantId')
    const savedUserId = localStorage.getItem('userId')
    const savedPlatformAdminKey = localStorage.getItem('platformAdminKey')

    if (savedTenantId) setTenantIdState(savedTenantId)
    if (savedUserId) setUserIdState(savedUserId)
    if (savedPlatformAdminKey) setPlatformAdminKeyState(savedPlatformAdminKey)
  }, [])

  const setTenantId = (id: string | null) => {
    setTenantIdState(id)
    if (id) {
      localStorage.setItem('tenantId', id)
    } else {
      localStorage.removeItem('tenantId')
    }
  }

  const setUserId = (id: string | null) => {
    setUserIdState(id)
    if (id) {
      localStorage.setItem('userId', id)
    } else {
      localStorage.removeItem('userId')
    }
  }

  const setPlatformAdminKey = (key: string | null) => {
    setPlatformAdminKeyState(key)
    if (key) {
      localStorage.setItem('platformAdminKey', key)
    } else {
      localStorage.removeItem('platformAdminKey')
    }
  }

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
