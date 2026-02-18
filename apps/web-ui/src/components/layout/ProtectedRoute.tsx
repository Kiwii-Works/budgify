import React from 'react'
import { Navigate } from 'react-router-dom'

interface ProtectedRouteProps {
  children: React.ReactNode
  requiredFields?: ('tenantId' | 'userId')[]
}

// Para esta primera versión, todas las rutas son accesibles
// En una versión real aquí iría la lógica de autenticación
export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  return <>{children}</>
}
