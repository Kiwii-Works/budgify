import React, { useState } from 'react'
import { DashboardLayout } from '../components/layout/DashboardLayout'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Button, Input, Alert, Tabs } from '../components/ui'
import { useSession } from '../context/SessionContext'

const TestingPanel: React.FC = () => {
  const { tenantId, userId, platformAdminKey, setTenantId, setUserId, setPlatformAdminKey } = useSession()

  const [tempTenantId, setTempTenantId] = useState(tenantId || '')
  const [tempUserId, setTempUserId] = useState(userId || '')
  const [tempAdminKey, setTempAdminKey] = useState(platformAdminKey || '')

  const handleSaveSession = () => {
    if (tempTenantId) setTenantId(tempTenantId)
    if (tempUserId) setUserId(tempUserId)
    if (tempAdminKey) setPlatformAdminKey(tempAdminKey)
  }

  const mockCredentials = [
    { name: 'Platform Admin Key', value: 'super-secret-admin-key' },
    { name: 'Demo Tenant ID', value: '550e8400-e29b-41d4-a716-446655440000' },
    { name: 'Demo User ID', value: '550e8400-e29b-41d4-a716-446655440001' },
  ]

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }

  const tabs = [
    {
      label: 'Headers de Sesión',
      value: 'session',
      content: (
        <Card>
          <CardHeader>
            <CardTitle>Gestionar Headers de Testing</CardTitle>
            <CardDescription>
              Configura manualmente los headers para testing sin autenticación real
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
            <Button onClick={handleSaveSession}>Guardar Headers</Button>
          </CardFooter>
        </Card>
      ),
    },
    {
      label: 'Credenciales Demo',
      value: 'credentials',
      content: (
        <Card>
          <CardHeader>
            <CardTitle>Valores de Prueba</CardTitle>
            <CardDescription>Usa estos valores para testing rápido</CardDescription>
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
                    Copiar
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      ),
    },
    {
      label: 'Estado Actual',
      value: 'status',
      content: (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Sesión Actual</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <p className="text-sm text-slate-600">X-Tenant-Id</p>
                <p className="font-mono text-sm bg-slate-100 p-2 rounded break-all">
                  {tenantId || '❌ No configurado'}
                </p>
              </div>
              <div>
                <p className="text-sm text-slate-600">X-User-Id</p>
                <p className="font-mono text-sm bg-slate-100 p-2 rounded break-all">
                  {userId || '❌ No configurado'}
                </p>
              </div>
              <div>
                <p className="text-sm text-slate-600">X-Platform-Admin-Key</p>
                <p className="font-mono text-sm bg-slate-100 p-2 rounded break-all">
                  {platformAdminKey || '❌ No configurado'}
                </p>
              </div>
            </CardContent>
          </Card>

          <Alert variant="info">
            💡 Los headers configurados aquí se enviarán automáticamente con todas las requests a la API.
          </Alert>
        </div>
      ),
    },
  ]

  return (
    <DashboardLayout title="Testing Panel">
      <div className="space-y-6">
        <Alert variant="warning">
          ⚠️ Este panel es solo para desarrollo y testing. Los valores aquí se guardan en localStorage.
        </Alert>

        <Tabs tabs={tabs} />
      </div>
    </DashboardLayout>
  )
}

export default TestingPanel
