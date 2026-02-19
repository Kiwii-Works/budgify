import React, { useState } from 'react'
import { DashboardLayout } from '../components/layout/DashboardLayout'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Button, Tabs, Alert } from '../components/ui'
import { useSession } from '../context/SessionContext'
import { healthService } from '../services/api.service'
import FinancePage from './FinancePage'

// Dashboard home page
const DashboardPage: React.FC = () => {
  const { tenantId, userId } = useSession()
  const [healthStatus, setHealthStatus] = useState<string>('')
  const [loading, setLoading] = useState(false)

  // Check API health status
  const checkHealth = async () => {
    setLoading(true)
    try {
      const result = await healthService.check()
      setHealthStatus(result.status)
    } catch (error) {
      setHealthStatus('error')
    } finally {
      setLoading(false)
    }
  }

  // Tab configuration
  const tabs = [
    {
      label: 'Session Info',
      value: 'info',
      content: (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Current Session</CardTitle>
              <CardDescription>Connected session information</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <p className="text-sm text-slate-600">Tenant ID</p>
                <p className="font-mono text-sm bg-slate-100 p-2 rounded">{tenantId || 'Not configured'}</p>
              </div>
              <div>
                <p className="text-sm text-slate-600">User ID</p>
                <p className="font-mono text-sm bg-slate-100 p-2 rounded">{userId || 'Not configured'}</p>
              </div>
            </CardContent>
          </Card>
        </div>
      ),
    },
    {
      label: 'API Health',
      value: 'health',
      content: (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>API Status</CardTitle>
              <CardDescription>Check backend connection</CardDescription>
            </CardHeader>
            <CardContent>
              {healthStatus && (
                <Alert variant={healthStatus === 'ok' ? 'success' : 'error'} className="mb-4">
                  {healthStatus === 'ok' ? '✓ API is running correctly' : '✕ Error connecting to API'}
                </Alert>
              )}
            </CardContent>
            <CardFooter>
              <Button onClick={checkHealth} isLoading={loading}>
                Check Status
              </Button>
            </CardFooter>
          </Card>
        </div>
      ),
    }
  ]

  return (
    <DashboardLayout title="Dashboard">
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Welcome to Budgify</CardTitle>
            <CardDescription>Your budget management platform</CardDescription>
          </CardHeader>
        </Card>

        <Tabs tabs={tabs} />
      </div>
    </DashboardLayout>
  )
}

export default DashboardPage
