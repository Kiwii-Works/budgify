import React from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthLayout } from '../components/layout/AuthLayout'
import { LoginForm } from '../components/auth/LoginForm'

// Login page component
const LoginPage: React.FC = () => {
  const navigate = useNavigate()

  return (
    <AuthLayout title="Sign In" subtitle="Access your Budgify account">
      <LoginForm onSuccess={() => navigate('/dashboard')} />
    </AuthLayout>
  )
}

export default LoginPage
