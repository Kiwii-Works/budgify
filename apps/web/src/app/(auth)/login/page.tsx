'use client';

import Link from 'next/link';
import { Mail, Lock, Info } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { ROUTES } from '@/lib/config/constants';

export default function LoginPage() {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Login functionality will be implemented in Phase 2
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
                disabled
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
                disabled
              />
            </div>
            <p className="text-xs text-slate-500">
              Your password must be at least 8 characters
            </p>
          </div>

          {/* Phase 2 Notice */}
          <div className="rounded-lg border border-indigo-200 bg-indigo-50 p-4">
            <div className="flex gap-3">
              <Info className="mt-0.5 h-5 w-5 shrink-0 text-indigo-600" />
              <div>
                <p className="text-sm font-medium text-indigo-900">
                  Coming in Phase 2
                </p>
                <p className="mt-1 text-xs text-indigo-700">
                  Login functionality will be available after JWT authentication
                  is implemented.
                </p>
              </div>
            </div>
          </div>
        </CardContent>

        <CardFooter className="flex flex-col space-y-4 pt-6">
          <Button type="submit" className="w-full" size="lg" disabled>
            Sign in
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
