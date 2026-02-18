import React from 'react'
import { clsx } from 'clsx'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helpText?: string
}

// Reusable input field component with label and error messages
export const Input: React.FC<InputProps> = ({ label, error, helpText, className, ...props }) => {
  return (
    <div className="w-full">
      {label && <label className="form-label">{label}</label>}
      <input
        className={clsx('input-field', error && 'focus:ring-error-500 border-error-300', className)}
        {...props}
      />
      {error && <p className="text-error-500 text-sm mt-1">{error}</p>}
      {helpText && <p className="text-slate-500 text-sm mt-1">{helpText}</p>}
    </div>
  )
}
