import React from 'react'
import { clsx } from 'clsx'

interface CardProps {
  className?: string
  children: React.ReactNode
}

export const Card: React.FC<CardProps> = ({ className, children }) => (
  <div className={clsx('card p-6', className)}>{children}</div>
)

export const CardHeader: React.FC<{ children: React.ReactNode; className?: string }> = ({
  children,
  className,
}) => <div className={clsx('mb-4 pb-4 border-b border-slate-200', className)}>{children}</div>

export const CardTitle: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <h2 className="text-2xl font-semibold text-slate-900">{children}</h2>
)

export const CardDescription: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <p className="text-sm text-slate-600 mt-1">{children}</p>
)

export const CardContent: React.FC<{ children: React.ReactNode; className?: string }> = ({
  children,
  className,
}) => <div className={className}>{children}</div>

export const CardFooter: React.FC<{ children: React.ReactNode; className?: string }> = ({
  children,
  className,
}) => <div className={clsx('pt-4 border-t border-slate-200 flex gap-3', className)}>{children}</div>
