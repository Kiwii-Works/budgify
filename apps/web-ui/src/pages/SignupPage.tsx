import React from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthLayout } from '../components/layout/AuthLayout'
import { SignupForm } from '../components/auth/SignupForm'

// User registration page component
const SignupPage: React.FC = () => {
  const navigate = useNavigate()

  return (
    <AuthLayout title="Create Account" subtitle="Join Budgify">
      <SignupForm onSuccess={() => navigate('/dashboard')} />
    </AuthLayout>
  )
}

export default SignupPage
