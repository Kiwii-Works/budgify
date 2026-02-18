import React from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthLayout } from '../components/layout/AuthLayout'
import { ForgotPasswordForm } from '../components/auth/ForgotPasswordForm'

const ForgotPasswordPage: React.FC = () => {
  const navigate = useNavigate()

  return (
    <AuthLayout title="Recuperar Contraseña" subtitle="Restablece tu contraseña">
      <ForgotPasswordForm onSuccess={() => navigate('/login')} />
    </AuthLayout>
  )
}

export default ForgotPasswordPage
