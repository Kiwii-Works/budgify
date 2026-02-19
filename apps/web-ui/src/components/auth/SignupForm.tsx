import React, { useState } from 'react'
import { Button, Input, Alert } from '../ui'
import { useSession } from '../../context/SessionContext'

interface SignupFormProps {
  onSuccess?: () => void
}

// User signup form component
export const SignupForm: React.FC<SignupFormProps> = ({ onSuccess }) => {
  const { setTenantId, setUserId } = useSession()
  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    password: '',
    confirmPassword: '',
    tenant_id: '',
  })
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    // Validate tenant ID is provided
    if (!formData.tenant_id) {
      setError('Please enter a tenant ID')
      return
    }

    setIsLoading(true)
    try {
      const { userService } = await import('../../services/api.service')
      const response = await userService.register(
        {
          username: formData.username,
          first_name: formData.first_name,
          last_name: formData.last_name,
          email: formData.email,
          phone_number: formData.phone_number || undefined,
          password: formData.password,
        },
        formData.tenant_id,
      )
      setTenantId(formData.tenant_id)
      setUserId(response.user_id)
      onSuccess?.()
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Signup failed'
      setError(message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <Alert variant="error">{error}</Alert>}

      <Input
        type="text"
        label="Username"
        placeholder="username"
        name="username"
        value={formData.username}
        onChange={handleChange}
        required
      />

      <div className="grid grid-cols-2 gap-4">
        <Input
          type="text"
          label="First Name"
          placeholder="John"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
          required
        />
        <Input
          type="text"
          label="Last Name"
          placeholder="Doe"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
          required
        />
      </div>

      <Input
        type="email"
        label="Email"
        placeholder="user@example.com"
        name="email"
        value={formData.email}
        onChange={handleChange}
        required
      />

      <Input
        type="tel"
        label="Phone (optional)"
        placeholder="+1 234 567 8900"
        name="phone_number"
        value={formData.phone_number}
        onChange={handleChange}
      />

      <Input
        type="text"
        label="Tenant ID"
        placeholder="Enter tenant ID"
        name="tenant_id"
        value={formData.tenant_id}
        onChange={handleChange}
        required
      />

      <Input
        type="password"
        label="Password"
        placeholder="••••••••"
        name="password"
        value={formData.password}
        onChange={handleChange}
        required
      />

      <Input
        type="password"
        label="Confirm Password"
        placeholder="••••••••"
        name="confirmPassword"
        value={formData.confirmPassword}
        onChange={handleChange}
        required
      />

      <Button type="submit" fullWidth isLoading={isLoading}>
        Create Account
      </Button>

      <div className="text-center border-t pt-4">
        <p className="text-slate-600 text-sm">
          Already have an account?{' '}
          <a href="/login" className="text-primary-600 hover:text-primary-700 font-medium">
            Sign in
          </a>
        </p>
      </div>
    </form>
  )
}
