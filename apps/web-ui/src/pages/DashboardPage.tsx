import React, { useState } from 'react'
import { DashboardLayout } from '../components/layout/DashboardLayout'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Button, Tabs, Alert } from '../components/ui'
import { useSession } from '../context/SessionContext'
import { healthService } from '../services/api.service'

const DashboardPage: React.FC = () => {
  const { tenantId, userId } = useSession()
  const [healthStatus, setHealthStatus] = useState<string>('')
  const [loading, setLoading] = useState(false)

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

  const tabs = [
    {
      label: 'Información',
      value: 'info',
      content: (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Sesión Actual</CardTitle>
              <CardDescription>Información de la sesión conectada</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <p className="text-sm text-slate-600">Tenant ID</p>
                <p className="font-mono text-sm bg-slate-100 p-2 rounded">{tenantId || 'No configurado'}</p>
              </div>
              <div>
                <p className="text-sm text-slate-600">User ID</p>
                <p className="font-mono text-sm bg-slate-100 p-2 rounded">{userId || 'No configurado'}</p>
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
              <CardTitle>Estado de la API</CardTitle>
              <CardDescription>Verifica la conexión con el backend</CardDescription>
            </CardHeader>
            <CardContent>
              {healthStatus && (
                <Alert variant={healthStatus === 'ok' ? 'success' : 'error'} className="mb-4">
                  {healthStatus === 'ok' ? '✓ API está funcionando correctamente' : '✕ Error conectando con la API'}
                </Alert>
              )}
            </CardContent>
            <CardFooter>
              <Button onClick={checkHealth} isLoading={loading}>
                Verificar Estado
              </Button>
            </CardFooter>
          </Card>
        </div>
      ),
    },
  ]

  return (
    <DashboardLayout title="Dashboard">
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Bienvenido a Budgify</CardTitle>
            <CardDescription>Tu plataforma de gestión de presupuestos</CardDescription>
          </CardHeader>
        </Card>

        <Tabs tabs={tabs} />
      </div>
    </DashboardLayout>
  )
}

export default DashboardPage
