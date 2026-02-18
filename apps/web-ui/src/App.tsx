import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { SessionProvider } from './context/SessionContext'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import ForgotPasswordPage from './pages/ForgotPasswordPage'
import DashboardPage from './pages/DashboardPage'
import TenantsPage from './pages/TenantsPage'
import UsersPage from './pages/UsersPage'
import TestingPanel from './pages/TestingPanel'

function App() {
  return (
    <Router>
      <SessionProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/tenants" element={<TenantsPage />} />
          <Route path="/users" element={<UsersPage />} />
          <Route path="/testing" element={<TestingPanel />} />
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </SessionProvider>
    </Router>
  )
}

export default App
