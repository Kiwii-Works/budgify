'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Mail, Lock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert } from '@/components/ui/alert';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { ROUTES } from '@/lib/config/constants';
import { useAuth } from '@/context/AuthContext';
import { apiClient } from '@/lib/api/client';

interface Tenant {
  tenant_id: string;
  name: string;
}

export default function LoginPage() {
  const router = useRouter();
  const { login, error, isLoading, clearError, isAuthenticated } = useAuth();

  // State
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [tenantId, setTenantId] = useState('');
  const [availableTenants, setAvailableTenants] = useState<Tenant[]>([]);
  const [tenantsLoading, setTenantsLoading] = useState(false);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      router.push(ROUTES.DASHBOARD);
    }
  }, [isAuthenticated, router]);

  // Fetch available tenants on component mount
  useEffect(() => {
    const fetchTenants = async () => {
      setTenantsLoading(true);
      try {
        const response = await apiClient.get<{ data: Tenant[] }>('/api/platform/tenants');
        const tenants = response.data.data;
        setAvailableTenants(tenants);

        // Set first tenant as default if only one available
        if (tenants.length === 1) {
          setTenantId(tenants[0].tenant_id);
        }
      } catch (err) {
        console.error('Failed to fetch tenants:', err);
      } finally {
        setTenantsLoading(false);
      }
    };

    fetchTenants();
  }, []);

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();

    if (!email || !password || !tenantId) {
      return;
    }

    try {
      await login(email, password, tenantId);
      router.push(ROUTES.DASHBOARD);
    } catch (err) {
      // Error is already set in auth context
      console.error('Login failed:', err);
    }
  };

  // Clear error when user starts typing
  const handleEmailChange = (value: string) => {
    setEmail(value);
    if (error) clearError();
  };

  const handlePasswordChange = (value: string) => {
    setPassword(value);
    if (error) clearError();
  };

  return (
    <Card className="shadow-lg">
      <CardHeader className="space-y-1 pb-6">
        <CardTitle className="text-2xl font-bold">Welcome back</CardTitle>
        <CardDescription className="text-base">
          Sign in to your account to continue
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-5">
          {/* Error Alert */}
          {error && (
            <Alert
              variant="destructive"
              title="Login Error"
              description={error}
            />
          )}

          {/* Email */}
          <div className="space-y-2">
            <Label htmlFor="email" className="text-sm font-medium">
              Email address
            </Label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
              <Input
                id="email"
                type="email"
                placeholder="john@example.com"
                className="pl-10"
                value={email}
                onChange={(e) => handleEmailChange(e.target.value)}
                disabled={isLoading || tenantsLoading}
                required
              />
            </div>
            <p className="text-xs text-slate-500">
              Enter the email you used to register
            </p>
          </div>

          {/* Password */}
          <div className="space-y-2">
            <Label htmlFor="password" className="text-sm font-medium">
              Password
            </Label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                className="pl-10"
                value={password}
                onChange={(e) => handlePasswordChange(e.target.value)}
                disabled={isLoading || tenantsLoading}
                required
              />
            </div>
            <p className="text-xs text-slate-500">
              Your password must be at least 8 characters
            </p>
          </div>

          {/* Tenant Select */}
          <div className="space-y-2">
            <Label htmlFor="tenant" className="text-sm font-medium">
              Select Tenant
            </Label>
            <select
              id="tenant"
              value={tenantId}
              onChange={(e) => {
                setTenantId(e.target.value);
                if (error) clearError();
              }}
              disabled={isLoading || tenantsLoading}
              className="h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm placeholder:text-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
              required
            >
              <option value="">
                {tenantsLoading ? 'Loading tenants...' : 'Choose a tenant...'}
              </option>
              {availableTenants.map((tenant) => (
                <option key={tenant.tenant_id} value={tenant.tenant_id}>
                  {tenant.name}
                </option>
              ))}
            </select>
          </div>
        </CardContent>

        <CardFooter className="flex flex-col space-y-4 pt-6">
          <Button 
            type="submit" 
            className="w-full" 
            size="lg" 
            disabled={isLoading || tenantsLoading || !tenantId}
          >
            {isLoading ? 'Signing in...' : 'Sign in'}
          </Button>
          <div className="flex flex-col space-y-2 text-center text-sm">
            <Link
              href={ROUTES.FORGOT_PASSWORD}
              className="text-slate-600 transition-colors hover:text-indigo-600 hover:underline"
            >
              Forgot password?
            </Link>
            <p className="text-slate-600">
              Don't have an account?{' '}
              <Link
                href={ROUTES.SIGNUP}
                className="font-medium text-indigo-600 transition-colors hover:text-indigo-700 hover:underline"
              >
                Sign up
              </Link>
            </p>
          </div>
        </CardFooter>
      </form>
    </Card>
  );
}
