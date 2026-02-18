import React from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthLayout } from '../components/layout/AuthLayout'
import { SignupForm } from '../components/auth/SignupForm'

const SignupPage: React.FC = () => {
  const navigate = useNavigate()

  return (
    <AuthLayout title="Crear Cuenta" subtitle="Únete a Budgify">
      <SignupForm onSuccess={() => navigate('/dashboard')} />
    </AuthLayout>
  )
}

export default SignupPage
