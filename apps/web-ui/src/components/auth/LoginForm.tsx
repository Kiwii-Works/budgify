import React, { useState } from 'react'
import { Button, Input, Alert } from '../ui'

interface LoginFormProps {
  onSuccess?: () => void
}

// Login form component
export const LoginForm: React.FC<LoginFormProps> = ({ onSuccess }) => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      // TODO: Implement actual authentication with backend
      if (email && password) {
        localStorage.setItem('accessToken', 'mock-token')
        localStorage.setItem('refreshToken', 'mock-refresh-token')
        onSuccess?.()
      } else {
        setError('Please fill in all fields')
      }
    } catch (err: any) {
      setError(err.message || 'Login failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <Alert variant="error">{error}</Alert>}

      <Input
        type="email"
        label="Email"
        placeholder="user@example.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />

      <Input
        type="password"
        label="Password"
        placeholder="••••••••"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />

      <Button type="submit" fullWidth isLoading={isLoading}>
        Sign In
      </Button>

      <div className="text-center">
        <a href="/forgot-password" className="text-primary-600 hover:text-primary-700 text-sm">
          Forgot your password?
        </a>
      </div>

      <div className="text-center border-t pt-4">
        <p className="text-slate-600 text-sm">
          Don't have an account?{' '}
          <a href="/signup" className="text-primary-600 hover:text-primary-700 font-medium">
            Sign up
          </a>
        </p>
      </div>
    </form>
  )
}
