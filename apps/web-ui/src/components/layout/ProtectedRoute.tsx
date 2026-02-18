import React from 'react'
import { Navigate } from 'react-router-dom'

interface ProtectedRouteProps {
  children: React.ReactNode
  requiredFields?: ('tenantId' | 'userId')[]
}

// Route wrapper for protected pages
// TODO: Implement actual authentication checking logic
export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  // For now, all routes are accessible
  // In production, add authentication validation here
  return <>{children}</>
}
