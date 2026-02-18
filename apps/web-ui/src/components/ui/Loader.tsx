import React from 'react'
interface LoaderProps {
  size?: 'sm' | 'md' | 'lg'
  fullScreen?: boolean
}

export const Loader: React.FC<LoaderProps> = ({ size = 'md', fullScreen = false }) => {
  const sizeClass = {
    sm: 'w-6 h-6 border-2',
    md: 'w-12 h-12 border-4',
    lg: 'w-16 h-16 border-4',
  }[size]

  const loader = (
    <div className={`${sizeClass} border-slate-300 border-t-primary-600 rounded-full animate-spin`} />
  )

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
        {loader}
      </div>
    )
  }

  return <div className="flex justify-center items-center">{loader}</div>
}
