# Budgify Web UI

Aplicación React + Vite profesional y moderna para gestionar la plataforma Budgify.

## 🚀 Características

- ✅ **Autenticación Completa**: Login, Signup, Recuperar Contraseña
- ✅ **Gestión de Tenants**: Crear y administrar tenants
- ✅ **Gestión de Usuarios**: Registrar, actualizar y gestionar usuarios
- ✅ **Testing Panel**: Configurar manualmente headers para testing sin autenticación real
- ✅ **UI Moderna**: Diseño profesional con Tailwind CSS
- ✅ **TypeScript**: Código totalmente tipado
- ✅ **Client API**: Integración con todos los endpoints del backend

## 📋 Tecnologías

- **React 18** - UI Library
- **TypeScript** - Type Safety
- **Vite** - Build tool y dev server
- **Tailwind CSS** - Utility-first CSS
- **Axios** - HTTP client
- **React Router** - Routing
- **TanStack Query** - Data fetching (preparado para futuro)

## 🛠️ Setup

### Requisitos
- Node.js 18+
- npm 9+

### Instalación

```bash
cd apps/web-ui
npm install
```

### Desarrollo

```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

### Build

```bash
npm run build
```

## 📁 Estructura del Proyecto

```
src/
├── components/
│   ├── ui/                 # Componentes de UI reutilizables
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   ├── Alert.tsx
│   │   ├── Modal.tsx
│   │   ├── Tabs.tsx
│   │   └── Loader.tsx
│   ├── layout/             # Layouts principales
│   │   ├── AuthLayout.tsx
│   │   ├── DashboardLayout.tsx
│   │   ├── Sidebar.tsx
│   │   └── ProtectedRoute.tsx
│   └── auth/               # Componentes de autenticación
│       ├── LoginForm.tsx
│       ├── SignupForm.tsx
│       └── ForgotPasswordForm.tsx
├── pages/                  # Páginas de la aplicación
│   ├── LoginPage.tsx
│   ├── SignupPage.tsx
│   ├── ForgotPasswordPage.tsx
│   ├── DashboardPage.tsx
│   ├── TenantsPage.tsx
│   ├── UsersPage.tsx
│   └── TestingPanel.tsx
├── services/               # Servicios API
│   └── api.service.ts
├── lib/                    # Utilidades y configuración
│   └── api.ts              # Cliente Axios configurado
├── context/                # React Context
│   └── SessionContext.tsx
├── types/                  # Tipos TypeScript
│   └── index.ts
├── App.tsx                 # Componente raíz
├── main.tsx                # Punto de entrada
└── index.css               # Estilos globales
```

## 🔑 Funcionalidades

### 🔐 Autenticación
- **Login**: Accede con email y contraseña
- **Signup**: Regístrate como nuevo usuario (requiere Tenant ID)
- **Forgot Password**: Recupera tu contraseña

### 🏢 Tenants
- Crear nuevos tenants (requiere Platform Admin Key)
- Asignar admin inicial al tenant
- Gestión centralizada de todos los tenants

### 👥 Usuarios
- Registrar nuevos usuarios en un tenant
- Actualizar información de usuario
- Activar/desactivar usuarios

### 🧪 Testing Panel
- Configure manualmente `X-Tenant-Id`
- Configure manualmente `X-User-Id`
- Configure manualmente `X-Platform-Admin-Key`
- Los valores se guardan en localStorage y se usan automáticamente en todas las requests

## 📡 API Integration

Todos los endpoints del backend están integrados:

- `GET /api/health` - Verificar estado de la API
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refrescar token
- `POST /api/auth/logout` - Logout
- `POST /api/platform/tenants` - Crear tenant
- `POST /api/auth/register` - Registrar usuario
- `PATCH /api/admin/users/{user_id}` - Actualizar usuario
- `PATCH /api/admin/users/{user_id}/activate` - Activar/desactivar usuario

## 🔄 Headers Automáticos

El cliente Axios envía automáticamente estos headers basado en la sesión:

```
X-Tenant-Id: {tenantId from localStorage}
X-User-Id: {userId from localStorage}
X-Platform-Admin-Key: {platformAdminKey from localStorage}
Authorization: Bearer {accessToken}
X-Request-Id: {auto-generated}
```

## 💾 LocalStorage

La aplicación usa localStorage para persistir:

- `tenantId` - ID del tenant actual
- `userId` - ID del usuario actual
- `platformAdminKey` - Clave de admin para operaciones privilegiadas
- `accessToken` - Token JWT de autenticación
- `refreshToken` - Token para refrescar accessToken

## 🎨 Temas de Componentes

### Botones
- `primary` - Azul principal
- `secondary` - Gris
- `ghost` - Sin fondo
- `danger` - Rojo

### Alertas
- `success` - Verde
- `error` - Rojo
- `warning` - Amarillo
- `info` - Azul

## 📱 Responsive

La aplicación es completamente responsive y funciona perfectamente en:
- Desktop
- Tablet
- Mobile

## 🚦 Flujos Implementados

### 1. Flujo de Login
```
Login Page → Validar credenciales → Guardar tokens → Dashboard
```

### 2. Flujo de Signup
```
Signup Page → Registrar usuario en tenant → Guardar credenciales → Dashboard
```

### 3. Flujo de Tenants
```
Testing Panel (set admin key) → Tenants Page → Crear tenant → Usuario admin creado
```

### 4. Flujo de Usuarios
```
Testing Panel (set tenant/user) → Users Page → Registrar/Actualizar → API
```

## 🔧 Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
VITE_API_URL=http://localhost:8000
```

## 📝 Próximas Mejoras

- [ ] Implementar autenticación real con JWT
- [ ] Agregar más modelos y CRUD
- [ ] Dashboard con gráficos y estadísticas
- [ ] Búsqueda y filtros avanzados
- [ ] Paginación mejorada
- [ ] Notificaciones en tiempo real
- [ ] Dark mode
- [ ] Multi-idioma

## 🐛 Reporte de Errores

Si encuentras bugs, por favor reportalos en el issue tracker del proyecto.

## 📄 Licencia

Propiedad de Budgify © 2024
