import React, { useState } from 'react'
import { DashboardLayout } from '../components/layout/DashboardLayout'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Button, Input, Alert, Modal } from '../components/ui'
import { useSession } from '../context/SessionContext'
import { tenantService, userService } from '../services/api.service'

const TenantsPage: React.FC = () => {
  const { platformAdminKey, setTenantId, setUserId } = useSession()
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [formData, setFormData] = useState({
    tenant_name: '',
    admin_username: '',
    admin_first_name: '',
    admin_last_name: '',
    admin_email: '',
    admin_password: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleCreateTenant = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (!platformAdminKey) {
      setError('Platform Admin Key no configurada. Usa el Testing Panel.')
      return
    }

    setIsLoading(true)
    try {
      const response = await tenantService.create(
        {
          tenant_name: formData.tenant_name,
          initial_admin: {
            username: formData.admin_username,
            first_name: formData.admin_first_name,
            last_name: formData.admin_last_name,
            email: formData.admin_email,
            password: formData.admin_password,
          },
        },
        platformAdminKey
      )

      setTenantId(response.tenant_id)
      if (response.admin_user_id) {
        setUserId(response.admin_user_id)
      }

      setSuccess(`Tenant "${response.tenant_name}" creado exitosamente`)
      setFormData({
        tenant_name: '',
        admin_username: '',
        admin_first_name: '',
        admin_last_name: '',
        admin_email: '',
        admin_password: '',
      })
      setIsModalOpen(false)
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Error al crear tenant')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <DashboardLayout title="Gestión de Tenants">
      <div className="space-y-6">
        {error && <Alert variant="error" onClose={() => setError('')}>{error}</Alert>}
        {success && <Alert variant="success" onClose={() => setSuccess('')}>{success}</Alert>}

        <Card>
          <CardHeader>
            <CardTitle>Crear Nuevo Tenant</CardTitle>
            <CardDescription>Solo disponible con Platform Admin Key</CardDescription>
          </CardHeader>
          <CardFooter>
            <Button onClick={() => setIsModalOpen(true)} disabled={!platformAdminKey}>
              Crear Tenant
            </Button>
          </CardFooter>
        </Card>

        <Modal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          title="Crear Nuevo Tenant"
          size="lg"
        >
          <form onSubmit={handleCreateTenant} className="space-y-4">
            <Input
              label="Nombre del Tenant"
              placeholder="Mi Empresa"
              name="tenant_name"
              value={formData.tenant_name}
              onChange={handleChange}
              required
            />

            <div className="border-t pt-4">
              <h3 className="font-semibold text-slate-900 mb-4">Admin Inicial</h3>

              <Input
                label="Usuario"
                placeholder="admin"
                name="admin_username"
                value={formData.admin_username}
                onChange={handleChange}
                required
              />

              <div className="grid grid-cols-2 gap-4 mt-4">
                <Input
                  label="Nombre"
                  placeholder="Juan"
                  name="admin_first_name"
                  value={formData.admin_first_name}
                  onChange={handleChange}
                  required
                />
                <Input
                  label="Apellido"
                  placeholder="Pérez"
                  name="admin_last_name"
                  value={formData.admin_last_name}
                  onChange={handleChange}
                  required
                />
              </div>

              <Input
                label="Email"
                type="email"
                placeholder="admin@empresa.com"
                name="admin_email"
                value={formData.admin_email}
                onChange={handleChange}
                required
                className="mt-4"
              />

              <Input
                label="Contraseña"
                type="password"
                placeholder="••••••••"
                name="admin_password"
                value={formData.admin_password}
                onChange={handleChange}
                required
                className="mt-4"
              />
            </div>

            <div className="flex gap-3 justify-end pt-4">
              <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>
                Cancelar
              </Button>
              <Button type="submit" isLoading={isLoading}>
                Crear Tenant
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </DashboardLayout>
  )
}

export default TenantsPage
