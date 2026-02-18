import React, { useState } from 'react'
import { DashboardLayout } from '../components/layout/DashboardLayout'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Button, Input, Alert, Tabs } from '../components/ui'
import { useSession } from '../context/SessionContext'

// Testing panel for manual header configuration during development
const TestingPanel: React.FC = () => {\n  const { tenantId, userId, platformAdminKey, setTenantId, setUserId, setPlatformAdminKey } = useSession()

  // Local state for editing headers
  const [tempTenantId, setTempTenantId] = useState(tenantId || '')
  const [tempUserId, setTempUserId] = useState(userId || '')
  const [tempAdminKey, setTempAdminKey] = useState(platformAdminKey || '')

  // Save session headers to context and localStorage
  const handleSaveSession = () => {
    if (tempTenantId) setTenantId(tempTenantId)
    if (tempUserId) setUserId(tempUserId)
    if (tempAdminKey) setPlatformAdminKey(tempAdminKey)
  }

  // Mock credentials for quick testing
  const mockCredentials = [
    { name: 'Platform Admin Key', value: 'super-secret-admin-key' },
    { name: 'Demo Tenant ID', value: '550e8400-e29b-41d4-a716-446655440000' },
    { name: 'Demo User ID', value: '550e8400-e29b-41d4-a716-446655440001' },
  ]

  // Copy value to clipboard
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }

  // Tab configuration
  const tabs = [
    {
      label: 'Session Headers',
      value: 'session',
      content: (
        <Card>
          <CardHeader>
            <CardTitle>Manage Test Headers</CardTitle>
            <CardDescription>
              Configure headers manually for testing without real authentication
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              label="X-Tenant-Id"
              placeholder="550e8400-e29b-41d4-a716-446655440000"
              value={tempTenantId}
              onChange={(e) => setTempTenantId(e.target.value)}
            />

            <Input
              label="X-User-Id"
              placeholder="550e8400-e29b-41d4-a716-446655440001"
              value={tempUserId}
              onChange={(e) => setTempUserId(e.target.value)}
            />

            <Input
              label="X-Platform-Admin-Key"
              placeholder="super-secret-admin-key"
              value={tempAdminKey}
              onChange={(e) => setTempAdminKey(e.target.value)}
            />
          </CardContent>
          <CardFooter>
            <Button onClick={handleSaveSession}>Save Headers</Button>
          </CardFooter>
        </Card>
      ),
    },
    {
      label: 'Demo Credentials',
      value: 'credentials',
      content: (
        <Card>
          <CardHeader>
            <CardTitle>Test Values</CardTitle>
            <CardDescription>Use these values for quick testing</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {mockCredentials.map((cred, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-slate-50 rounded border border-slate-200">
                  <div>
                    <p className="text-sm font-medium text-slate-900">{cred.name}</p>
                    <p className="text-xs text-slate-600 font-mono break-all mt-1">{cred.value}</p>
                  </div>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => copyToClipboard(cred.value)}
                  >
                    Copy
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      ),
    },
    {
      label: 'Current Status',
      value: 'status',
      content: (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Current Session</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <p className="text-sm text-slate-600">X-Tenant-Id</p>
                <p className="font-mono text-sm bg-slate-100 p-2 rounded break-all">
                  {tenantId || '❌ Not configured'}
                </p>
              </div>
              <div>
                <p className="text-sm text-slate-600">X-User-Id</p>
                <p className="font-mono text-sm bg-slate-100 p-2 rounded break-all">
                  {userId || '❌ Not configured'}
                </p>
              </div>
              <div>
                <p className="text-sm text-slate-600">X-Platform-Admin-Key</p>
                <p className="font-mono text-sm bg-slate-100 p-2 rounded break-all">
                  {platformAdminKey || '❌ Not configured'}
                </p>
              </div>
            </CardContent>
          </Card>

          <Alert variant="info">
            💡 Headers configured here are automatically sent with all API requests.
          </Alert>
        </div>
      ),
    },
  ]

  return (
    <DashboardLayout title="Testing Panel">
      <div className="space-y-6">
        <Alert variant="warning">
          ⚠️ This panel is for development and testing only. Values are stored in localStorage.
        </Alert>

        <Tabs tabs={tabs} />
      </div>
    </DashboardLayout>
  )
}

export default TestingPanel
