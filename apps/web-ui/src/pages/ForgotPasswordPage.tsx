import React from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthLayout } from '../components/layout/AuthLayout'
import { ForgotPasswordForm } from '../components/auth/ForgotPasswordForm'

// Password recovery page component
const ForgotPasswordPage: React.FC = () => {
  const navigate = useNavigate()

  return (
    <AuthLayout title="Reset Password" subtitle="Recover your password">
      <ForgotPasswordForm onSuccess={() => navigate('/login')} />
    </AuthLayout>
  )
}

export default ForgotPasswordPage
