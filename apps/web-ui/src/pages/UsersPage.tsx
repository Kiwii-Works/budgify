import React, { useState } from 'react'
import { DashboardLayout } from '../components/layout/DashboardLayout'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Button, Input, Alert, Modal, Tabs } from '../components/ui'
import { useSession } from '../context/SessionContext'
import { userService } from '../services/api.service'

const UsersPage: React.FC = () => {
  const { tenantId, userId, setUserId } = useSession()
  const [isRegisterModalOpen, setIsRegisterModalOpen] = useState(false)
  const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false)
  const [selectedUserId, setSelectedUserId] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const [registerData, setRegisterData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    password: '',
  })

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

  const handleRegisterUser = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (!tenantId) {
      setError('Tenant ID no configurado')
      return
    }

    setIsLoading(true)
    try {
      const response = await userService.register(registerData, tenantId)
      setSuccess(`Usuario "${response.username}" registrado exitosamente`)
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
      setError(err.response?.data?.error?.message || 'Error al registrar usuario')
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpdateUser = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (!userId) {
      setError('User ID no configurado')
      return
    }

    setIsLoading(true)
    try {
      const response = await userService.update(selectedUserId, updateData, userId)
      setSuccess(`Usuario actualizado exitosamente`)
      setUpdateData({
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
      })
      setIsUpdateModalOpen(false)
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Error al actualizar usuario')
    } finally {
      setIsLoading(false)
    }
  }

  const tabs = [
    {
      label: 'Registrar Usuario',
      value: 'register',
      content: (
        <Card>
          <CardHeader>
            <CardTitle>Registrar Nuevo Usuario</CardTitle>
            <CardDescription>Agrega un nuevo usuario al tenant</CardDescription>
          </CardHeader>
          <CardFooter>
            <Button onClick={() => setIsRegisterModalOpen(true)} disabled={!tenantId}>
              Registrar Usuario
            </Button>
          </CardFooter>
        </Card>
      ),
    },
    {
      label: 'Actualizar Usuario',
      value: 'update',
      content: (
        <Card>
          <CardHeader>
            <CardTitle>Actualizar Información de Usuario</CardTitle>
            <CardDescription>Edita los datos de un usuario existente</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              label="User ID a Actualizar"
              placeholder="Ingresa el UUID del usuario"
              value={selectedUserId}
              onChange={(e) => setSelectedUserId(e.target.value)}
            />
          </CardContent>
          <CardFooter>
            <Button
              onClick={() => setIsUpdateModalOpen(true)}
              disabled={!userId || !selectedUserId}
            >
              Abrir Formulario
            </Button>
          </CardFooter>
        </Card>
      ),
    },
  ]

  return (
    <DashboardLayout title="Gestión de Usuarios">
      <div className="space-y-6">
        {error && <Alert variant="error" onClose={() => setError('')}>{error}</Alert>}
        {success && <Alert variant="success" onClose={() => setSuccess('')}>{success}</Alert>}

        <Tabs tabs={tabs} />

        {/* Register Modal */}
        <Modal
          isOpen={isRegisterModalOpen}
          onClose={() => setIsRegisterModalOpen(false)}
          title="Registrar Nuevo Usuario"
          size="lg"
        >
          <form onSubmit={handleRegisterUser} className="space-y-4">
            <Input
              label="Nombre de Usuario"
              placeholder="usuario"
              name="username"
              value={registerData.username}
              onChange={handleRegisterChange}
              required
            />

            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Nombre"
                placeholder="Juan"
                name="first_name"
                value={registerData.first_name}
                onChange={handleRegisterChange}
                required
              />
              <Input
                label="Apellido"
                placeholder="Pérez"
                name="last_name"
                value={registerData.last_name}
                onChange={handleRegisterChange}
                required
              />
            </div>

            <Input
              label="Email"
              type="email"
              placeholder="usuario@ejemplo.com"
              name="email"
              value={registerData.email}
              onChange={handleRegisterChange}
              required
            />

            <Input
              label="Teléfono (opcional)"
              placeholder="+34 600 000 000"
              name="phone_number"
              value={registerData.phone_number}
              onChange={handleRegisterChange}
            />

            <Input
              label="Contraseña"
              type="password"
              placeholder="••••••••"
              name="password"
              value={registerData.password}
              onChange={handleRegisterChange}
              required
            />

            <div className="flex gap-3 justify-end pt-4">
              <Button type="button" variant="secondary" onClick={() => setIsRegisterModalOpen(false)}>
                Cancelar
              </Button>
              <Button type="submit" isLoading={isLoading}>
                Registrar
              </Button>
            </div>
          </form>
        </Modal>

        {/* Update Modal */}
        <Modal
          isOpen={isUpdateModalOpen}
          onClose={() => setIsUpdateModalOpen(false)}
          title="Actualizar Usuario"
          size="lg"
        >
          <form onSubmit={handleUpdateUser} className="space-y-4">
            <p className="text-sm text-slate-600">
              Actualizando usuario: <code className="bg-slate-100 px-2 py-1 rounded">{selectedUserId.slice(0, 8)}...</code>
            </p>

            <Input
              label="Nombre"
              placeholder="Juan"
              name="first_name"
              value={updateData.first_name}
              onChange={handleUpdateChange}
            />

            <Input
              label="Apellido"
              placeholder="Pérez"
              name="last_name"
              value={updateData.last_name}
              onChange={handleUpdateChange}
            />

            <Input
              label="Email"
              type="email"
              placeholder="usuario@ejemplo.com"
              name="email"
              value={updateData.email}
              onChange={handleUpdateChange}
            />

            <Input
              label="Teléfono"
              placeholder="+34 600 000 000"
              name="phone_number"
              value={updateData.phone_number}
              onChange={handleUpdateChange}
            />

            <div className="flex gap-3 justify-end pt-4">
              <Button type="button" variant="secondary" onClick={() => setIsUpdateModalOpen(false)}>
                Cancelar
              </Button>
              <Button type="submit" isLoading={isLoading}>
                Actualizar
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </DashboardLayout>
  )
}

export default UsersPage
