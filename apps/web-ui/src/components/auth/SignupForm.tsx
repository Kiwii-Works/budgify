import React, { useState } from 'react'
import { Button, Input, Alert } from '../ui'
import { useSession } from '../../context/SessionContext'

interface SignupFormProps {
  onSuccess?: () => void
}

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

    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden')
      return
    }

    if (!formData.tenant_id) {
      setError('Por favor ingresa el ID del tenant')
      return
    }

    setIsLoading(true)
    try {
      // TODO: Implement actual signup with API
      // const response = await userService.register({...}, tenant_id)
      
      // Mock success
      setTenantId(formData.tenant_id)
      setUserId('mock-user-id')
      localStorage.setItem('accessToken', 'mock-token')
      onSuccess?.()
    } catch (err: any) {
      setError(err.message || 'Error al registrarse')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <Alert variant="error">{error}</Alert>}

      <Input
        type="text"
        label="Nombre de Usuario"
        placeholder="usuario"
        name="username"
        value={formData.username}
        onChange={handleChange}
        required
      />

      <div className="grid grid-cols-2 gap-4">
        <Input
          type="text"
          label="Nombre"
          placeholder="Juan"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
          required
        />
        <Input
          type="text"
          label="Apellido"
          placeholder="Pérez"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
          required
        />
      </div>

      <Input
        type="email"
        label="Email"
        placeholder="usuario@ejemplo.com"
        name="email"
        value={formData.email}
        onChange={handleChange}
        required
      />

      <Input
        type="tel"
        label="Teléfono (opcional)"
        placeholder="+34 600 000 000"
        name="phone_number"
        value={formData.phone_number}
        onChange={handleChange}
      />

      <Input
        type="text"
        label="ID del Tenant"
        placeholder="Ingresa el ID del tenant"
        name="tenant_id"
        value={formData.tenant_id}
        onChange={handleChange}
        required
      />

      <Input
        type="password"
        label="Contraseña"
        placeholder="••••••••"
        name="password"
        value={formData.password}
        onChange={handleChange}
        required
      />

      <Input
        type="password"
        label="Confirmar Contraseña"
        placeholder="••••••••"
        name="confirmPassword"
        value={formData.confirmPassword}
        onChange={handleChange}
        required
      />

      <Button type="submit" fullWidth isLoading={isLoading}>
        Crear Cuenta
      </Button>

      <div className="text-center border-t pt-4">
        <p className="text-slate-600 text-sm">
          ¿Ya tienes cuenta?{' '}
          <a href="/login" className="text-primary-600 hover:text-primary-700 font-medium">
            Inicia sesión
          </a>
        </p>
      </div>
    </form>
  )
}
