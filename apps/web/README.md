# Budgify Web App (Phase UI-1)

Next.js frontend for Budgify budget management application.

## Features

- ✅ Sign up page (functional, calls Phase 1B backend)
- ✅ Login page (UI shell - Phase 2)
- ✅ Forgot password page (UI shell - Phase 2)
- ✅ Protected dashboard with sidebar layout
- ✅ Settings page (placeholder)
- ✅ Temporary session management (localStorage)
- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Toast notifications (sonner)
- ✅ Form validation (react-hook-form + zod)

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **UI Components**: shadcn/ui
- **Icons**: lucide-react
- **Forms**: react-hook-form + zod
- **Notifications**: sonner
- **HTTP Client**: Fetch API

## Prerequisites

- Node.js 18+
- npm or yarn
- Budgify API running on http://localhost:8000

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

App will be available at http://localhost:3000

## Configuration

Create a `.env.local` file (copy from `.env.local.example`):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Budgify
```

## Usage Guide

### 1. Create a Tenant (Backend)

```bash
curl -X POST http://localhost:8000/api/platform/tenants \
  -H "X-Platform-Admin-Key: change-me" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_name": "My Company",
    "initial_admin": {
      "username": "admin",
      "first_name": "Admin",
      "last_name": "User",
      "email": "admin@company.com",
      "phone_number": "+1234567890",
      "password": "password123"
    }
  }'
```

### 2. Sign Up

Navigate to http://localhost:3000/signup and register with the tenant_id from step 1.

### 3. Access Dashboard

After signup, you'll be redirected to `/dashboard`.

## Project Structure

```
apps/web/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # Auth pages
│   │   ├── dashboard/         # Dashboard pages
│   │   ├── layout.tsx         # Root layout
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   ├── layout/            # Layout components
│   │   └── ui/                # shadcn/ui components
│   ├── lib/
│   │   ├── api/               # API client
│   │   ├── auth/              # Session management
│   │   └── config/            # Constants
│   └── types/                 # TypeScript types
└── public/                    # Static assets
```

## Development Scripts

```bash
npm run dev        # Start development server
npm run build      # Build for production
npm start          # Start production server
npm run lint       # Run ESLint
```

## API Integration

Communicates with Budgify API (Phase 1B):

- `POST /api/auth/register` - User registration
  - Header: `X-Tenant-Id`
  - Returns: user_id, username, email

## Known Limitations (Phase UI-1)

- Login not functional (Phase 2)
- Forgot password not functional (Phase 2)
- JWT authentication not implemented (Phase 2)
- Temporary localStorage session (replaced in Phase 2)

## Next Steps (Phase 2)

- Implement JWT authentication
- Connect login/forgot password to backend
- Add refresh token handling
- Implement RBAC UI

## License

Proprietary - Budgify Project
