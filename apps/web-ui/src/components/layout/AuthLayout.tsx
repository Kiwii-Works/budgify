import React from 'react'

interface AuthLayoutProps {
  children: React.ReactNode
  title: string
  subtitle?: string
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({ children, title, subtitle }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">Budgify</h1>
          <p className="text-slate-500">Budget Management Platform</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8 border border-slate-200">
          <h2 className="text-2xl font-bold text-slate-900 mb-1">{title}</h2>
          {subtitle && <p className="text-slate-600 text-sm mb-6">{subtitle}</p>}
          {children}
        </div>

        <p className="text-center text-slate-600 text-sm mt-6">
          © 2024 Budgify. Todos los derechos reservados.
        </p>
      </div>
    </div>
  )
}
