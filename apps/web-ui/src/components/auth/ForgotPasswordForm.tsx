import React, { useState } from 'react'
import { Button, Input, Alert } from '../ui'

interface ForgotPasswordFormProps {
  onSuccess?: () => void
}

// Password reset request form
export const ForgotPasswordForm: React.FC<ForgotPasswordFormProps> = ({ onSuccess }) => {
  const [email, setEmail] = useState('')
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      // TODO: Implement actual password reset with API
      // await authService.requestPasswordReset(email)
      
      setIsSubmitted(true)
      onSuccess?.()
    } catch (err: any) {
      setError(err.message || 'Failed to reset password')
    } finally {
      setIsLoading(false)
    }
  }

  // Show success message
  if (isSubmitted) {
    return (
      <div className="space-y-4">
        <Alert variant="success">
          Password reset link has been sent to {email}. Please check your email.
        </Alert>
        <Button fullWidth variant="secondary" onClick={() => (window.location.href = '/login')}>
          Back to Login
        </Button>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <Alert variant="error">{error}</Alert>}

      <p className="text-slate-600 text-sm">
        Enter your email address and we'll send you instructions to reset your password.
      </p>

      <Input
        type="email"
        label="Email"
        placeholder="user@example.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />

      <Button type="submit" fullWidth isLoading={isLoading}>
        Send Reset Link
      </Button>

      <div className="text-center">
        <a href="/login" className="text-primary-600 hover:text-primary-700 text-sm">
          Back to sign in
        </a>
      </div>
    </form>
  )
}
