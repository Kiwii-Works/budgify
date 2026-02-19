import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { clsx } from 'clsx'

// Navigation links for the sidebar
const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: '📊' },
  { name: 'Tenants', href: '/tenants', icon: '🏢' },
  { name: 'Users', href: '/users', icon: '👥' },
  { name: 'Finance', href: '/finance', icon: '💸' },
  { name: 'Testing', href: '/testing', icon: '🧪' },
]

// Left sidebar navigation component
export const Sidebar: React.FC = () => {
  const location = useLocation()

  return (
    <div className="w-64 bg-slate-900 text-white min-h-screen p-6">
      {/* Logo and branding */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Budgify</h1>
        <p className="text-slate-400 text-sm">Budget Manager</p>
      </div>

      {/* Navigation menu */}
      <nav className="space-y-2">
        {navigation.map((item) => (
          <Link
            key={item.href}
            to={item.href}
            className={clsx(
              'flex items-center gap-3 px-4 py-3 rounded-lg transition-colors',
              location.pathname === item.href
                ? 'bg-primary-600 text-white'
                : 'text-slate-300 hover:bg-slate-800'
            )}
          >
            <span className="text-lg">{item.icon}</span>
            {item.name}
          </Link>
        ))}
      </nav>
    </div>
  )
}
