import React from 'react'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
  footer?: React.ReactNode
  size?: 'sm' | 'md' | 'lg'
}

// Modal dialog component for overlays and forms
const sizeClasses = {
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-lg',
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
  size = 'md',
}) => {
  // Don't render if modal is closed
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className={`bg-white rounded-lg shadow-xl ${sizeClasses[size]} w-full mx-4`}>
        {/* Modal header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200">
          <h2 className="text-xl font-semibold">{title}</h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 text-2xl leading-none"
          >
            ×
          </button>
        </div>
        {/* Modal body */}
        <div className="p-6">{children}</div>
        {/* Modal footer */}
        {footer && <div className="px-6 py-4 bg-slate-50 border-t border-slate-200">{footer}</div>}
      </div>
    </div>
  )
}
