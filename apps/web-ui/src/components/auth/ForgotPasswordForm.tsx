import React, { useState } from 'react'
import { Button, Input, Alert } from '../ui'

interface ForgotPasswordFormProps {
  onSuccess?: () => void
}

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
      // TODO: Implement actual forgot password with API
      // await authService.requestPasswordReset(email)
      
      setIsSubmitted(true)
      onSuccess?.()
    } catch (err: any) {
      setError(err.message || 'Error al solicitar reinicio de contraseña')
    } finally {
      setIsLoading(false)
    }
  }

  if (isSubmitted) {
    return (
      <div className="space-y-4">
        <Alert variant="success">
          Se ha enviado un enlace de reinicio de contraseña a {email}. Por favor revisa tu correo.
        </Alert>
        <Button fullWidth variant="secondary" onClick={() => (window.location.href = '/login')}>
          Volver al Login
        </Button>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <Alert variant="error">{error}</Alert>}

      <p className="text-slate-600 text-sm">
        Ingresa tu correo electrónico y te enviaremos instrucciones para reiniciar tu contraseña.
      </p>

      <Input
        type="email"
        label="Email"
        placeholder="usuario@ejemplo.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />

      <Button type="submit" fullWidth isLoading={isLoading}>
        Enviar Enlace de Reinicio
      </Button>

      <div className="text-center">
        <a href="/login" className="text-primary-600 hover:text-primary-700 text-sm">
          Volver al inicio de sesión
        </a>
      </div>
    </form>
  )
}
