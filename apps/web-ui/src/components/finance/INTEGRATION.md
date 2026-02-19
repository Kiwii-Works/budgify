# Integración de Finance en la Aplicación Principal

Esta guía muestra cómo integrar la página de Finance en tu aplicación principal.

## 1. Integración Básica en el Router

Si estás usando React Router, agrega la ruta a tu configuración de rutas:

```tsx
// src/App.tsx o tu archivo de rutas
import { FinancePage } from './pages'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Router>
      <Routes>
        {/* Otras rutas... */}
        <Route path="/finance" element={<FinancePage />} />
      </Routes>
    </Router>
  )
}

export default App
```

## 2. Agregar Enlace en el Menú de Navegación

Agrega un enlace a la sección de finanzas en tu menú principal:

```tsx
// src/components/layout/Navigation.tsx
import { Link } from 'react-router-dom'

export const Navigation = () => {
  return (
    <nav>
      {/* Otros enlaces... */}
      <Link to="/finance" className="nav-link">
        Finanzas
      </Link>
    </nav>
  )
}
```

## 3. Proteger la Ruta con Autenticación

Asegúrate de que solo usuarios autenticados puedan acceder:

```tsx
// src/components/PrivateRoute.tsx
import { Navigate } from 'react-router-dom'
import { useSession } from './hooks/useSession'

interface PrivateRouteProps {
  component: React.ComponentType
}

export const PrivateRoute: React.FC<PrivateRouteProps> = ({
  component: Component,
}) => {
  const { userId, tenantId } = useSession()

  if (!userId || !tenantId) {
    return <Navigate to="/login" replace />
  }

  return <Component />
}

// Luego en tu router:
<Route 
  path="/finance" 
  element={<PrivateRoute component={FinancePage} />} 
/>
```

## 4. Integración con Contexto de Sesión

Los componentes de Finance utilizan automáticamente el contexto de sesión para obtener `tenantId` y `userId` del localStorage.

Asegúrate de que tu contexto de sesión está configurado correctamente:

```tsx
// src/context/SessionContext.tsx
import { createContext, useState } from 'react'

export interface SessionContextType {
  tenantId: string | null
  userId: string | null
  platformAdminKey: string | null
  setTenantId: (id: string | null) => void
  setUserId: (id: string | null) => void
  setPlatformAdminKey: (key: string | null) => void
  clearSession: () => void
}

export const SessionContext = createContext<SessionContextType | undefined>(undefined)

export const SessionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [tenantId, setTenantId] = useState<string | null>(
    localStorage.getItem('tenantId')
  )
  const [userId, setUserId] = useState<string | null>(
    localStorage.getItem('userId')
  )
  const [platformAdminKey, setPlatformAdminKey] = useState<string | null>(
    localStorage.getItem('platformAdminKey')
  )

  const value: SessionContextType = {
    tenantId,
    userId,
    platformAdminKey,
    setTenantId: (id) => {
      setTenantId(id)
      if (id) localStorage.setItem('tenantId', id)
      else localStorage.removeItem('tenantId')
    },
    setUserId: (id) => {
      setUserId(id)
      if (id) localStorage.setItem('userId', id)
      else localStorage.removeItem('userId')
    },
    setPlatformAdminKey: (key) => {
      setPlatformAdminKey(key)
      if (key) localStorage.setItem('platformAdminKey', key)
      else localStorage.removeItem('platformAdminKey')
    },
    clearSession: () => {
      setTenantId(null)
      setUserId(null)
      setPlatformAdminKey(null)
      localStorage.removeItem('tenantId')
      localStorage.removeItem('userId')
      localStorage.removeItem('platformAdminKey')
    },
  }

  return (
    <SessionContext.Provider value={value}>
      {children}
    </SessionContext.Provider>
  )
}
```

## 5. Hook Personalizado para Sesión

Crea un hook reutilizable para acceder a los datos de sesión:

```tsx
// src/hooks/useSession.ts
import { useContext } from 'react'
import { SessionContext } from '../context/SessionContext'

export const useSession = () => {
  const context = useContext(SessionContext)
  if (!context) {
    throw new Error('useSession debe usarse dentro de SessionProvider')
  }
  return context
}
```

## 6. Ejemplo de Dashboard Completo

Aquí está un ejemplo de cómo podría verse tu dashboard con Finance integrado:

```tsx
// src/pages/DashboardPage.tsx
import { useState } from 'react'
import { FinancePage } from './FinancePage'
import { useSession } from '../hooks/useSession'

export const DashboardPage = () => {
  const { tenantId, userId } = useSession()
  const [activeSection, setActiveSection] = useState('overview')

  if (!tenantId || !userId) {
    return <div>Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold">Budgify</h1>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setActiveSection('overview')}
                className={`${
                  activeSection === 'overview'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600'
                }`}
              >
                Resumen
              </button>
              <button
                onClick={() => setActiveSection('finance')}
                className={`${
                  activeSection === 'finance'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600'
                }`}
              >
                Finanzas
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Content */}
      <main>
        {activeSection === 'overview' && (
          <div className="max-w-7xl mx-auto py-6 px-4">
            <h2 className="text-2xl font-bold">Resumen del Dashboard</h2>
            {/* Contenido del resumen */}
          </div>
        )}
        {activeSection === 'finance' && <FinancePage />}
      </main>
    </div>
  )
}
```

## 7. Variables de Entorno

Asegúrate de que tienes configurada la URL de la API:

```env
# .env
VITE_API_URL=http://localhost:8000
```

## 8. Instalación de Dependencias

Asegúrate de que axios está instalado:

```bash
npm install axios
```

## 9. Estructura de Carpetas Esperada

```
src/
├── components/
│   ├── finance/          # Componentes de Finance
│   │   ├── AccountForm.tsx
│   │   ├── AccountsList.tsx
│   │   ├── CategoryForm.tsx
│   │   ├── CategoriesList.tsx
│   │   ├── TransactionForm.tsx
│   │   ├── TransactionsList.tsx
│   │   ├── index.ts
│   │   └── README.md
│   └── layout/
├── pages/
│   ├── FinancePage.tsx
│   └── index.ts
├── services/
│   ├── api.service.ts
│   └── finance.service.ts
├── types/
│   └── index.ts
└── App.tsx
```

## 10. Prueba la Integración

Una vez integrado, puedes probar:

1. Navega a `/finance` en tu aplicación
2. Crea una categoría
3. Crea una cuenta asociada a la categoría
4. Crea una transacción asociada a la cuenta
5. Verifica que todos los datos se muestren correctamente en los listados

## Notas Finales

- La autenticación debe estar en lugar antes de acceder a Finance
- El `tenantId` y `userId` deben estar en localStorage
- La API debe estar corriendo en `http://localhost:8000` (o la URL configurada en `VITE_API_URL`)
- Todos los formularios validan datos antes de enviar
- Los listados pueden filtrar y ordenar automáticamente

## Soporte

Si encuentras problemas:

1. Verifica que todos los endpoints del API están disponibles
2. Desde de que la sesión tiene valores correctos en localStorage
3. Abre la consola del navegador para ver errores detallados
4. Revisa el archivo README.md en `src/components/finance/` para más detalles
