# 🚀 Guía de Uso - Budgify Web UI

Instrucciones para usar la aplicación web de Budgify.

## ⚡ Quick Start

### 1. Iniciar el servidor de desarrollo

```bash
cd apps/web-ui
npm run dev
```

La aplicación estará disponible en: **http://localhost:5173**

### 2. Configurar el Testing Panel

Antes de probar los endpoints, debes configurar los headers de testing:

1. Ve a http://localhost:5173
2. La página te redirigirá a `/login`
3. Haz clic en cualquier botón para acceder al dashboard (en dev no hay validación real)
4. Ve al menú de la sidebar y selecciona **🧪 Testing**
5. Configura los headers:
   - **X-Platform-Admin-Key**: `super-secret-admin-key`
   - **X-Tenant-Id**: `550e8400-e29b-41d4-a716-446655440000` (puedes usar cualquier UUID)
   - **X-User-Id**: `550e8400-e29b-41d4-a716-446655440001` (puedes usar cualquier UUID)

## 📋 Flujos de Testing

### 1. **Verificar API Health** ✓ Estado de la API
- Ve a **Dashboard**
- Tab "API Health"
- Haz clic en "Verificar Estado"
- Deberás ver "✓ API está funcionando correctamente"

### 2. **Crear un Tenant** 🏢
- Ve a **Tenants**
- Haz clic en "Crear Tenant"
- Llena el formulario:
  - **Nombre del Tenant**: Ej. "Mi Empresa"
  - **Admin Username**: Ej. "admin"
  - **Admin Nombre**: Juan
  - **Admin Apellido**: Pérez
  - **Admin Email**: admin@empresa.com
  - **Admin Contraseña**: password123
- Haz clic en "Crear Tenant"
- El nuevo Tenant ID se guardará en la sesión

### 3. **Registrar un Usuario en el Tenant** 👤
- Ve a **Usuarios**
- Tab "Registrar Usuario"
- Haz clic en "Registrar Usuario"
- Llena el formulario:
  - **Username**: ej_usuario
  - **Nombre**: Carlos
  - **Apellido**: López
  - **Email**: carlos@empresa.com
  - **Teléfono**: +34 600 000 000 (opcional)
  - **Contraseña**: password123
- Haz clic en "Registrar"

### 4. **Actualizar Información de Usuario** ✏️
- Ve a **Usuarios**
- Tab "Actualizar Usuario"
- Ingresa el User ID que deseas actualizar
- Haz clic en "Abrir Formulario"
- Modifica los campos que desees
- Haz clic en "Actualizar"

## 🔑 Headers Automáticos

Una vez configures los valores en el Testing Panel, se enviarán automáticamente con cada request:

```
X-Tenant-Id: {valor configurado}
X-User-Id: {valor configurado}
X-Platform-Admin-Key: {valor configurado}
Authorization: Bearer {token si está disponible}
X-Request-Id: {auto-generado}
```

Los valores se guardan en localStorage y persisten entre sesiones.

## 📱 Navegación

### Sidebar (Izquierda)
- **📊 Dashboard**: Panel principal con información de sesión
- **🏢 Tenants**: Gestión de tenants (solo con admin key)
- **👥 Usuarios**: Gestión de usuarios (requiere tenant ID)
- **🧪 Testing**: Configurar headers para testing

### Menú Auth (sin autenticación real)
- **🔐 Login**: Acceso (no validado en dev)
- **📝 Signup**: Registro
- **🔑 Forgot Password**: Recuperar contraseña

## 🎯 Casos de Uso Recomendados

### Caso 1: Crear Tenants y Usuarios
```
1. Testing Panel → Configurar X-Platform-Admin-Key
2. Tenants → Crear Tenant nuevo
3. Testing Panel → Actualizar X-Tenant-Id con el nuevo tenant
4. Usuarios → Registrar usuario en el tenant
5. Verificar en Testing Panel que todo está configurado
```

### Caso 2: Gestionar Usuarios
```
1. Testing Panel → Configurar X-Tenant-Id y X-User-Id
2. Usuarios → Registrar más usuarios
3. Usuarios → Actualizar información de usuarios existentes
4. Dashboard → Verificar conexión a API
```

### Caso 3: Verificar Estado
```
1. Dashboard → API Health
2. Verificar que la API responde correctamente
3. Testing Panel → Ver resumen de sesión actual
```

## 🐛 Solución de Problemas

### "Error conectando con la API"
- Verifica que el servidor backend esté ejecutándose en http://localhost:8000
- Revisa la consola del navegador (F12) para ver más detalles del error

### "Platform Admin Key no configurada"
- Ve al Testing Panel
- Configura X-Platform-Admin-Key
- Guarda los headers
- Recarga la página

### "Error al crear tenant"
- Verifica que X-Platform-Admin-Key sea correcta
- Comprueba que el email del admin no exista ya
- Revisa la consola para ver el mensaje de error específico

### "No se envían requests a la API"
- Abre la pestaña "Network" en las herramientas de desarrollo
- Verifica si se está haciendo la request
- Si no aparece, revisa que X-Tenant-Id esté configurado correctamente

## 📊 Estados Guardados en LocalStorage

```javascript
{
  "tenantId": "550e8400-e29b-41d4-a716-446655440000",
  "userId": "550e8400-e29b-41d4-a716-446655440001",
  "platformAdminKey": "super-secret-admin-key",
  "accessToken": "mock-token", // Se actualiza con login real
  "refreshToken": "mock-refresh-token" // Se actualiza con login real
}
```

Puedes limpiar estos valores en el Testing Panel o ejecutando:
```javascript
localStorage.clear()
```

## 🔐 Notas Sobre Seguridad

⚠️ **ESTO ES SOLO PARA DESARROLLO**

- No hay validación real de contraseñas
- Los tokens son ficticios (mock)
- Los headers se guardan en texto plano en localStorage
- Nunca uses esto en producción

En producción:
- Implementar autenticación real con JWT
- Usar HttpOnly cookies para tokens
- Validar tokens en el backend
- Implementar CSRF protection

## ✅ Checklist de Funcionalidades

- [x] Login/Signup/Forgot Password UI
- [x] Dashboard con estado de API
- [x] Gestión de Tenants
- [x] Gestión de Usuarios
- [x] Testing Panel para headers
- [x] Cliente API con Axios
- [x] Context para sesión
- [x] Componentes UI reutilizables
- [x] Tailwind CSS + Responsive
- [x] TypeScript en todo el proyecto
- [x] Build production-ready

## 🔄 Desarrollo Futuro

- [ ] Autenticación real con JWT
- [ ] Refresh token automático
- [ ] Logout real
- [ ] Dashboard mejorado con gráficos
- [ ] CRUD completo para todos los recursos
- [ ] Búsqueda y filtros avanzados
- [ ] Paginación mejorada
- [ ] Notificaciones en tiempo real
- [ ] Dark mode
- [ ] Multi-idioma
- [ ] Pruebas unitarias e integración
- [ ] Documentación de componentes

## 📞 Soporte

Para reportar bugs o sugerencias, contacta al equipo de desarrollo.

---

**Happy Testing! 🎉**
