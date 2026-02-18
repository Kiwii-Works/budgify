import React, { useState } from 'react'
import { DashboardLayout } from '../components/layout/DashboardLayout'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Button, Input, Alert, Modal } from '../components/ui'
import { useSession } from '../context/SessionContext'
import { tenantService, userService } from '../services/api.service'

// Tenant management page
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

  // Create new tenant with initial admin
  const handleCreateTenant = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (!platformAdminKey) {
      setError('Platform Admin Key not configured. Use the Testing Panel.')
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

      setSuccess(`Tenant "${response.tenant_name}" created successfully`)
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
      setError(err.response?.data?.error?.message || 'Error creating tenant')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <DashboardLayout title="Tenant Management">
      <div className="space-y-6">
        {error && <Alert variant="error" onClose={() => setError('')}>{error}</Alert>}
        {success && <Alert variant="success" onClose={() => setSuccess('')}>{success}</Alert>}

        <Card>
          <CardHeader>
            <CardTitle>Create New Tenant</CardTitle>
            <CardDescription>Only available with Platform Admin Key</CardDescription>
          </CardHeader>
          <CardFooter>
            <Button onClick={() => setIsModalOpen(true)} disabled={!platformAdminKey}>
              Create Tenant
            </Button>
          </CardFooter>
        </Card>

        <Modal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          title="Create New Tenant"
          size="lg"
        >
          <form onSubmit={handleCreateTenant} className="space-y-4">
            <Input
              label="Tenant Name"
              placeholder="My Company"
              name="tenant_name"
              value={formData.tenant_name}
              onChange={handleChange}
              required
            />

            <div className="border-t pt-4">
              <h3 className="font-semibold text-slate-900 mb-4">Initial Admin</h3>

              <Input
                label="Username"
                placeholder="admin"
                name="admin_username"
                value={formData.admin_username}
                onChange={handleChange}
                required
              />

              <div className="grid grid-cols-2 gap-4 mt-4">
                <Input
                  label="First Name"
                  placeholder="John"
                  name="admin_first_name"
                  value={formData.admin_first_name}
                  onChange={handleChange}
                  required
                />
                <Input
                  label="Last Name"
                  placeholder="Doe"
                  name="admin_last_name"
                  value={formData.admin_last_name}
                  onChange={handleChange}
                  required
                />
              </div>

              <Input
                label="Email"
                type="email"
                placeholder="admin@company.com"
                name="admin_email"
                value={formData.admin_email}
                onChange={handleChange}
                required
                className="mt-4"
              />

              <Input
                label="Password"
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
                Cancel
              </Button>
              <Button type="submit" isLoading={isLoading}>
                Create Tenant
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </DashboardLayout>
  )
}

export default TenantsPage
