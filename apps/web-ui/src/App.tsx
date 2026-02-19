import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { SessionProvider } from './context/SessionContext'

// Import pages with lazy loading for better performance
const LoginPage = React.lazy(() => import('./pages/LoginPage'))
const SignupPage = React.lazy(() => import('./pages/SignupPage'))
const ForgotPasswordPage = React.lazy(() => import('./pages/ForgotPasswordPage'))
const DashboardPage = React.lazy(() => import('./pages/DashboardPage'))
const TenantsPage = React.lazy(() => import('./pages/TenantsPage'))
const UsersPage = React.lazy(() => import('./pages/UsersPage'))
const TestingPanel = React.lazy(() => import('./pages/TestingPanel'))
const FinancePage = React.lazy(() => import('./pages/FinancePage'))

// Loading fallback component
const LoadingFallback = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="text-lg text-gray-600">Loading...</div>
  </div>
)

// Main application component with routing
function App() {
  return (
    <Router>
      <SessionProvider>
        <React.Suspense fallback={<LoadingFallback />}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/tenants" element={<TenantsPage />} />
            <Route path="/users" element={<UsersPage />} />
            <Route path="/testing" element={<TestingPanel />} />
            {/* Finance route */}
            <Route path="/finance" element={<FinancePage />} />
            {/* Default route redirect */}
            <Route path="/" element={<Navigate to="/login" replace />} />
          </Routes>
        </React.Suspense>
      </SessionProvider>
    </Router>
  )
}

export default App
