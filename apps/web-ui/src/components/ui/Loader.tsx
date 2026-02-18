import React from 'react'

interface LoaderProps {
  size?: 'sm' | 'md' | 'lg'
  fullScreen?: boolean
}

// Loading spinner component
export const Loader: React.FC<LoaderProps> = ({ size = 'md', fullScreen = false }) => {
  // Size variants for the spinner
  const sizeClass = {
    sm: 'w-6 h-6 border-2',
    md: 'w-12 h-12 border-4',
    lg: 'w-16 h-16 border-4',
  }[size]

  // Spinner element
  const loader = (
    <div className={`${sizeClass} border-slate-300 border-t-primary-600 rounded-full animate-spin`} />
  )

  // Show full-screen loader if requested
  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
        {loader}
      </div>
    )
  }

  // Show inline loader
  return <div className="flex justify-center items-center">{loader}</div>
}
