import React, { useState } from 'react'
import { Button, Input, Alert } from '../ui'
import { useSession } from '../../context/SessionContext'
import { authService } from '../../services/api.service'

interface LoginFormProps {
  onSuccess?: () => void
}

// Login form component
export const LoginForm: React.FC<LoginFormProps> = ({ onSuccess }) => {
  const { setTenantId, setUserId } = useSession()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [tenantId, setTenantIdField] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      const result = await authService.login(email, password, tenantId)
      localStorage.setItem('accessToken', result.access_token)
      localStorage.setItem('refreshToken', result.refresh_token)
      setTenantId(result.tenant_id)
      setUserId(result.user_id)
      onSuccess?.()
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Login failed'
      setError(message)
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

      <Input
        type="text"
        label="Tenant ID"
        placeholder="Enter your tenant ID"
        value={tenantId}
        onChange={(e) => setTenantIdField(e.target.value)}
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
