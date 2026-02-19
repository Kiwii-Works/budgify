# Finance Components - Web UI

Este directorio contiene todos los componentes de interfaz de usuario para gestionar finanzas en **web-ui** exclusivamente.

## Estructura

### Componentes

#### 1. **CategoryForm** (`CategoryForm.tsx`)
Formulario para crear y editar categorías de cuentas.

**Props:**
- `category?: AccountCategory` - Categoría a editar (opcional)
- `onSuccess: (category: AccountCategory) => void` - Callback cuando se guarda con éxito
- `onCancel: () => void` - Callback para cancelar
- `isLoading?: boolean` - Indica si está cargando

**Ejemplo:**
```tsx
<CategoryForm
  category={selectedCategory}
  onSuccess={handleCategorySuccess}
  onCancel={() => setShowForm(false)}
/>
```

#### 2. **CategoriesList** (`CategoriesList.tsx`)
Tabla con todas las categorías. Permite editar, eliminar y cambiar estado.

**Props:**
- `onEdit: (category: AccountCategory) => void` - Callback cuando se selecciona editar
- `onRefresh?: () => void` - Callback para refrescar datos
- `isLoading?: boolean` - Indica si está cargando

#### 3. **AccountForm** (`AccountForm.tsx`)
Formulario para crear y editar cuentas. Carga automáticamente las categorías activas.

**Props:**
- `account?: Account` - Cuenta a editar (opcional)
- `onSuccess: (account: Account) => void` - Callback cuando se guarda
- `onCancel: () => void` - Callback para cancelar
- `isLoading?: boolean` - Indica si está cargando

#### 4. **AccountsList** (`AccountsList.tsx`)
Tabla con todas las cuentas filtradas por tipo (Ingresos/Gastos).

**Props:**
- `onEdit: (account: Account) => void` - Callback cuando se selecciona editar
- `onRefresh?: () => void` - Callback para refrescar
- `isLoading?: boolean` - Indica si está cargando

#### 5. **TransactionForm** (`TransactionForm.tsx`)
Formulario para crear y editar transacciones. Carga automáticamente las cuentas activas.

**Props:**
- `transaction?: Transaction` - Transacción a editar (opcional)
- `onSuccess: (transaction: Transaction) => void` - Callback cuando se guarda
- `onCancel: () => void` - Callback para cancelar
- `isLoading?: boolean` - Indica si está cargando

#### 6. **TransactionsList** (`TransactionsList.tsx`)
Tabla con todas las transacciones, filtradas por tipo y ordenadas por fecha descendente.

**Props:**
- `onEdit: (transaction: Transaction) => void` - Callback cuando se selecciona editar
- `onRefresh?: () => void` - Callback para refrescar
- `isLoading?: boolean` - Indica si está cargando

## Servicios de API

### `finance.service.ts`

Contiene tres servicios principales:

#### 1. **accountCategoryService**
```typescript
- list(params?: FinancePaginationParams): Promise<AccountCategory[]>
- get(categoryId: string): Promise<AccountCategory>
- create(request: CreateAccountCategoryRequest): Promise<AccountCategory>
- update(categoryId: string, request: UpdateAccountCategoryRequest): Promise<AccountCategory>
- delete(categoryId: string): Promise<void>
```

#### 2. **accountService**
```typescript
- list(params?: FinancePaginationParams): Promise<Account[]>
- get(accountId: string): Promise<Account>
- create(request: CreateAccountRequest): Promise<Account>
- update(accountId: string, request: UpdateAccountRequest): Promise<Account>
- delete(accountId: string): Promise<void>
```

#### 3. **transactionService**
```typescript
- list(params?: FinancePaginationParams): Promise<Transaction[]>
- listByAccount(accountId: string, params?: FinancePaginationParams): Promise<Transaction[]>
- get(transactionId: string): Promise<Transaction>
- create(request: CreateTransactionRequest): Promise<Transaction>
- update(transactionId: string, request: UpdateTransactionRequest): Promise<Transaction>
- delete(transactionId: string): Promise<void>
```

## Tipos de Datos

Todos los tipos están definidos en `src/types/index.ts`:

### AccountCategory
```typescript
interface AccountCategory {
  category_id: string
  tenant_id: string
  name: string
  description?: string
  is_active: boolean
}
```

### Account
```typescript
interface Account {
  account_id: string
  tenant_id: string
  category_id: string
  name: string
  description?: string
  type: 'INCOME' | 'EXPENSE'
  is_active: boolean
}
```

### Transaction
```typescript
interface Transaction {
  transaction_id: string
  tenant_id: string
  account_id: string
  amount: number
  currency: string
  occurred_on: string
  notes?: string
  direction: 'INCOME' | 'EXPENSE'
  created_by: string
  created_date: string
  modified_by?: string
  modified_date?: string
}
```

## Página Principal - FinancePage

La página principal está disponible en `src/pages/FinancePage.tsx` e integra todos los componentes con un sistema de pestañas.

### Características:
- Sistema de pestañas para navegar entre Categorías, Cuentas y Transacciones
- Formularios integrados para crear y editar
- Listados con funciones de búsqueda, filtrado y eliminación
- Gestión de estado automática con refresh
- Manejo robusto de errores

### Uso:
```tsx
import { FinancePage } from './pages'

function App() {
  return <FinancePage />
}
```

## Flujo de Uso Típico

1. **Crear Categorías:**
   - Ir a la pestaña "Categorías"
   - Hacer clic en "+ Nueva Categoría"
   - Llenar el formulario y guardar

2. **Crear Cuentas:**
   - Ir a la pestaña "Cuentas"
   - Hacer clic en "+ Nueva Cuenta"
   - Seleccionar una categoría y tipo
   - Llenar el formulario y guardar

3. **Crear Transacciones:**
   - Ir a la pestaña "Transacciones"
   - Hacer clic en "+ Nueva Transacción"
   - Seleccionar una cuenta y moneda
   - Ingresar monto, fecha y notas
   - Guardar

## Características Implementadas

✅ CRUD completo para Categorías, Cuentas y Transacciones
✅ Carga automática de datos relacionados (categorías en formulario de cuentas, etc.)
✅ Filtrado por tipo (Ingresos/Gastos)
✅ Ordenamiento automático por fecha
✅ Formato de moneda localizado
✅ Validaciones en cliente
✅ Manejo de errores con reintentos
✅ Componentes reutilizables
✅ Interfaz responsiva con Tailwind CSS
✅ Estados visuales para carga y eliminación
✅ Confirmación antes de eliminar

## Endpoints del API Esperados

El frontend asume los siguientes endpoints:

```
GET    /api/finance/account-categories
POST   /api/finance/account-categories
GET    /api/finance/account-categories/:categoryId
PATCH  /api/finance/account-categories/:categoryId
DELETE /api/finance/account-categories/:categoryId

GET    /api/finance/accounts
POST   /api/finance/accounts
GET    /api/finance/accounts/:accountId
PATCH  /api/finance/accounts/:accountId
DELETE /api/finance/accounts/:accountId

GET    /api/finance/transactions
GET    /api/finance/accounts/:accountId/transactions
POST   /api/finance/transactions
GET    /api/finance/transactions/:transactionId
PATCH  /api/finance/transactions/:transactionId
DELETE /api/finance/transactions/:transactionId
```

## Notas Importantes

- Todos los componentes están pensados para funcionar **solo en web-ui**
- Los servicios usan el cliente API configurado en `src/lib/api.ts`
- Las transacciones se ordena automáticamente por fecha descendente
- Los montos se formatean automáticamente con la moneda especificada
- El estado de tenant se obtiene automáticamente del localStorage
