import React from 'react'

interface AlertProps {
  variant?: 'success' | 'error' | 'warning' | 'info'
  title?: string
  children: React.ReactNode
  onClose?: () => void
}

// Alert/notification component for displaying messages
export const Alert: React.FC<AlertProps> = ({
  variant = 'info',
  title,
  children,
  onClose,
}) => {
  // Color styles for each alert type
  const variantStyles = {
    success: 'bg-success-50 border-success-200 text-success-800',
    error: 'bg-error-50 border-error-200 text-error-800',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    info: 'bg-primary-50 border-primary-200 text-primary-800',
  }

  // Icons for each alert type
  const iconClass = {
    success: '✓',
    error: '✕',
    warning: '!',
    info: 'ℹ',
  }

  return (
    <div className={`border rounded-lg p-4 ${variantStyles[variant]} flex gap-3`}>
      <span className="text-lg font-bold flex-shrink-0">{iconClass[variant]}</span>
      <div className="flex-1">
        {title && <p className="font-semibold mb-1">{title}</p>}
        <p className="text-sm">{children}</p>
      </div>
      {onClose && (
        <button onClick={onClose} className="text-lg hover:opacity-70 flex-shrink-0">
          ✕
        </button>
      )}
    </div>
  )
}
