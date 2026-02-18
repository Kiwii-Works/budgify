import React, { useState, useCallback } from 'react'
import { Button, Input, Alert } from '../ui'

interface LoginFormProps {
  onSuccess?: () => void
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSuccess }) => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault()
      setError('')
      setIsLoading(true)

      try {
        // TODO: Implement actual login with API
        // const response = await authService.login(email, password)
        // localStorage.setItem('accessToken', response.access_token)
        // localStorage.setItem('refreshToken', response.refresh_token)
        
        // Mock success for now
        if (email && password) {
          localStorage.setItem('accessToken', 'mock-token')
          localStorage.setItem('refreshToken', 'mock-refresh-token')
          onSuccess?.()
        } else {
          setError('Por favor completa todos los campos')
        }
      } catch (err: any) {
        setError(err.message || 'Error al iniciar sesión')
      } finally {
        setIsLoading(false)
      }
    },
    [email, password, onSuccess]
  )

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <Alert variant="error">{error}</Alert>}

      <Input
        type="email"
        label="Email"
        placeholder="usuario@ejemplo.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />

      <Input
        type="password"
        label="Contraseña"
        placeholder="••••••••"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />

      <Button type="submit" fullWidth isLoading={isLoading}>
        Iniciar Sesión
      </Button>

      <div className="text-center">
        <a href="/forgot-password" className="text-primary-600 hover:text-primary-700 text-sm">
          ¿Olvidaste tu contraseña?
        </a>
      </div>

      <div className="text-center border-t pt-4">
        <p className="text-slate-600 text-sm">
          ¿No tienes cuenta?{' '}
          <a href="/signup" className="text-primary-600 hover:text-primary-700 font-medium">
            Regístrate
          </a>
        </p>
      </div>
    </form>
  )
}
