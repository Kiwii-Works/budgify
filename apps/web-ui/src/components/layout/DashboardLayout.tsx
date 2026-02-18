import React from 'react'
import { useSession } from '../../context/SessionContext'
import { Button } from '../ui'
import { Sidebar } from './Sidebar'

interface DashboardLayoutProps {
  children: React.ReactNode
  title: string
}

// Layout for dashboard pages with sidebar and header
export const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children, title }) => {
  const { clearSession, tenantId, userId } = useSession()

  // Handle user logout
  const handleLogout = () => {
    clearSession()
    window.location.href = '/login'
  }

  return (
    <div className="flex min-h-screen bg-slate-50">
      {/* Left sidebar navigation */}
      <Sidebar />

      {/* Main content area */}
      <div className="flex-1">
        {/* Header bar */}
        <header className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              {/* Page title */}
              <div>
                <h1 className="text-3xl font-bold text-slate-900">{title}</h1>
              </div>
              {/* Session info and logout button */}
              <div className="flex items-center gap-4">
                {tenantId && (
                  <div className="text-sm border-r border-slate-200 pr-4">
                    <p className="text-slate-600 text-xs">Tenant ID</p>
                    <p className="text-slate-900 font-mono text-xs break-all">{tenantId.slice(0, 12)}...</p>
                  </div>
                )}
                {userId && (
                  <div className="text-sm border-r border-slate-200 pr-4">
                    <p className="text-slate-600 text-xs">User ID</p>
                    <p className="text-slate-900 font-mono text-xs break-all">{userId.slice(0, 12)}...</p>
                  </div>
                )}
                <Button variant="ghost" onClick={handleLogout} size="sm">
                  Logout
                </Button>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="p-6">{children}</main>
      </div>
    </div>
  )
}
