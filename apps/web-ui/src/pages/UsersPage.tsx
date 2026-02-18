import React, { useState } from 'react'
import { DashboardLayout } from '../components/layout/DashboardLayout'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Button, Input, Alert, Modal, Tabs } from '../components/ui'
import { useSession } from '../context/SessionContext'
import { userService } from '../services/api.service'

// User management page
const UsersPage: React.FC = () => {
  const { tenantId, userId, setUserId } = useSession()
  const [isRegisterModalOpen, setIsRegisterModalOpen] = useState(false)
  const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false)
  const [selectedUserId, setSelectedUserId] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // Form state for user registration
  const [registerData, setRegisterData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    password: '',
  })

  // Form state for user update
  const [updateData, setUpdateData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
  })

  const handleRegisterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setRegisterData((prev) => ({ ...prev, [name]: value }))
  }

  const handleUpdateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setUpdateData((prev) => ({ ...prev, [name]: value }))
  }

  // Register new user in tenant
  const handleRegisterUser = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (!tenantId) {
      setError('Tenant ID not configured')
      return
    }

    setIsLoading(true)
    try {
      const response = await userService.register(registerData, tenantId)
      setSuccess(`User "${response.username}" registered successfully`)
      setRegisterData({
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
        password: '',
      })
      setIsRegisterModalOpen(false)
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Error registering user')
    } finally {
      setIsLoading(false)
    }
  }

  // Update existing user information
  const handleUpdateUser = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (!userId) {
      setError('User ID not configured')
      return
    }

    setIsLoading(true)
    try {
      const response = await userService.update(selectedUserId, updateData, userId)
      setSuccess(`User updated successfully`)
      setUpdateData({
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
      })
      setIsUpdateModalOpen(false)
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Error updating user')
    } finally {
      setIsLoading(false)
    }
  }

  // Tab configuration for register/update operations
  const tabs = [
    {
      label: 'Register User',
      value: 'register',
      content: (
        <Card>
          <CardHeader>
            <CardTitle>Register New User</CardTitle>
            <CardDescription>Add a new user to the tenant</CardDescription>
          </CardHeader>
          <CardFooter>
            <Button onClick={() => setIsRegisterModalOpen(true)} disabled={!tenantId}>
              Register User
            </Button>
          </CardFooter>
        </Card>
      ),
    },
    {
      label: 'Update User',
      value: 'update',
      content: (
        <Card>
          <CardHeader>
            <CardTitle>Update User Information</CardTitle>
            <CardDescription>Edit data for an existing user</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              label="User ID to Update"
              placeholder="Enter the user's UUID"
              value={selectedUserId}
              onChange={(e) => setSelectedUserId(e.target.value)}
            />
          </CardContent>
          <CardFooter>
            <Button
              onClick={() => setIsUpdateModalOpen(true)}
              disabled={!userId || !selectedUserId}
            >
              Open Form
            </Button>
          </CardFooter>
        </Card>
      ),
    },
  ]

  return (
    <DashboardLayout title="User Management">
      <div className="space-y-6">
        {error && <Alert variant="error" onClose={() => setError('')}>{error}</Alert>}
        {success && <Alert variant="success" onClose={() => setSuccess('')}>{success}</Alert>}

        <Tabs tabs={tabs} />

        {/* Register User Modal */}
        <Modal
          isOpen={isRegisterModalOpen}
          onClose={() => setIsRegisterModalOpen(false)}
          title="Register New User"
          size="lg"
        >
          <form onSubmit={handleRegisterUser} className="space-y-4">
            <Input
              label="Username"
              placeholder="username"
              name="username"
              value={registerData.username}
              onChange={handleRegisterChange}
              required
            />

            <div className="grid grid-cols-2 gap-4">
              <Input
                label="First Name"
                placeholder="John"
                name="first_name"
                value={registerData.first_name}
                onChange={handleRegisterChange}
                required
              />
              <Input
                label="Last Name"
                placeholder="Doe"
                name="last_name"
                value={registerData.last_name}
                onChange={handleRegisterChange}
                required
              />
            </div>

            <Input
              label="Email"
              type="email"
              placeholder="user@example.com"
              name="email"
              value={registerData.email}
              onChange={handleRegisterChange}
              required
            />

            <Input
              label="Phone (optional)"
              placeholder="+1 234 567 8900"
              name="phone_number"
              value={registerData.phone_number}
              onChange={handleRegisterChange}
            />

            <Input
              label="Password"
              type="password"
              placeholder="••••••••"
              name="password"
              value={registerData.password}
              onChange={handleRegisterChange}
              required
            />

            <div className="flex gap-3 justify-end pt-4">
              <Button type="button" variant="secondary" onClick={() => setIsRegisterModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" isLoading={isLoading}>
                Register
              </Button>
            </div>
          </form>
        </Modal>

        {/* Update User Modal */}
        <Modal
          isOpen={isUpdateModalOpen}
          onClose={() => setIsUpdateModalOpen(false)}
          title="Update User"
          size="lg"
        >
          <form onSubmit={handleUpdateUser} className="space-y-4">
            <p className="text-sm text-slate-600">
              Updating user: <code className="bg-slate-100 px-2 py-1 rounded">{selectedUserId.slice(0, 8)}...</code>
            </p>

            <Input
              label="First Name"
              placeholder="John"
              name="first_name"
              value={updateData.first_name}
              onChange={handleUpdateChange}
            />

            <Input
              label="Last Name"
              placeholder="Doe"
              name="last_name"
              value={updateData.last_name}
              onChange={handleUpdateChange}
            />

            <Input
              label="Email"
              type="email"
              placeholder="user@example.com"
              name="email"
              value={updateData.email}
              onChange={handleUpdateChange}
            />

            <Input
              label="Phone"
              placeholder="+1 234 567 8900"
              name="phone_number"
              value={updateData.phone_number}
              onChange={handleUpdateChange}
            />

            <div className="flex gap-3 justify-end pt-4">
              <Button type="button" variant="secondary" onClick={() => setIsUpdateModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" isLoading={isLoading}>
                Update
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </DashboardLayout>
  )
}

export default UsersPage
