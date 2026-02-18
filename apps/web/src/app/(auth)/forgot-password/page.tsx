'use client';

import Link from 'next/link';
import { Mail, Info } from 'lucide-react';
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

export default function ForgotPasswordPage() {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Password reset functionality will be implemented in Phase 2
  };

  return (
    <Card className="shadow-lg">
      <CardHeader className="space-y-1 pb-6">
        <CardTitle className="text-2xl font-bold">Reset your password</CardTitle>
        <CardDescription className="text-base">
          Enter your email and we'll send you a reset link
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

          {/* Phase 2 Notice */}
          <div className="rounded-lg border border-indigo-200 bg-indigo-50 p-4">
            <div className="flex gap-3">
              <Info className="mt-0.5 h-5 w-5 shrink-0 text-indigo-600" />
              <div>
                <p className="text-sm font-medium text-indigo-900">
                  Coming in Phase 2
                </p>
                <p className="mt-1 text-xs text-indigo-700">
                  Password reset functionality will be available after email
                  integration is implemented.
                </p>
              </div>
            </div>
          </div>
        </CardContent>

        <CardFooter className="flex flex-col space-y-4 pt-6">
          <Button type="submit" className="w-full" size="lg" disabled>
            Send reset link
          </Button>
          <Link
            href={ROUTES.LOGIN}
            className="text-center text-sm text-slate-600 transition-colors hover:text-indigo-600 hover:underline"
          >
            Back to login
          </Link>
        </CardFooter>
      </form>
    </Card>
  );
}
