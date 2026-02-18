import React from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthLayout } from '../components/layout/AuthLayout'
import { LoginForm } from '../components/auth/LoginForm'

const LoginPage: React.FC = () => {
  const navigate = useNavigate()

  return (
    <AuthLayout title="Iniciar Sesión" subtitle="Accede a tu cuenta de Budgify">
      <LoginForm onSuccess={() => navigate('/dashboard')} />
    </AuthLayout>
  )
}

export default LoginPage
