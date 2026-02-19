import React from 'react'

interface AlertProps {
  variant?: 'default' | 'destructive' | 'warning' | 'success'
  title?: string
  description?: string
  children?: React.ReactNode
  className?: string
}

export const Alert: React.FC<AlertProps> = ({
  variant = 'default',
  title,
  description,
  children,
  className = '',
}) => {
  const variantStyles = {
    default: 'bg-blue-50 border border-blue-200 text-blue-900',
    destructive: 'bg-red-50 border border-red-200 text-red-900',
    warning: 'bg-yellow-50 border border-yellow-200 text-yellow-900',
    success: 'bg-green-50 border border-green-200 text-green-900',
  }

  const titleStyles = {
    default: 'text-blue-800 font-semibold',
    destructive: 'text-red-800 font-semibold',
    warning: 'text-yellow-800 font-semibold',
    success: 'text-green-800 font-semibold',
  }

  const descriptionStyles = {
    default: 'text-blue-700',
    destructive: 'text-red-700',
    warning: 'text-yellow-700',
    success: 'text-green-700',
  }

  return (
    <div
      className={`rounded-md p-4 ${variantStyles[variant]} ${className}`}
      role="alert"
    >
      {title && (
        <h3 className={`${titleStyles[variant]} mb-1`}>{title}</h3>
      )}
      {description && (
        <p className={`${descriptionStyles[variant]} text-sm`}>{description}</p>
      )}
      {children && (
        <div className={`${descriptionStyles[variant]} text-sm`}>{children}</div>
      )}
    </div>
  )
}
