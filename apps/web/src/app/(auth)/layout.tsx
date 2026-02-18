'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Wallet, Check } from 'lucide-react';
import { isAuthenticated } from '@/lib/auth/session';
import { ROUTES } from '@/lib/config/constants';

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();

  useEffect(() => {
    // If already authenticated, redirect to dashboard
    if (isAuthenticated()) {
      router.push(ROUTES.DASHBOARD);
    }
  }, [router]);

  return (
    <div className="flex min-h-screen">
      {/* Branding Panel - Hidden on mobile, visible on desktop */}
      <div className="gradient-primary hidden flex-1 flex-col justify-center px-12 py-12 lg:flex">
        <div className="mx-auto w-full max-w-md">
          {/* Logo */}
          <div className="mb-8 flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/10 backdrop-blur-sm">
              <Wallet className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-white">Budgify</h1>
          </div>

          {/* Tagline */}
          <h2 className="mb-4 text-3xl font-bold text-white">
            Manage your budget with ease
          </h2>
          <p className="mb-12 text-lg text-indigo-200">
            Take control of your finances with powerful tracking and insights.
          </p>

          {/* Features */}
          <ul className="space-y-4">
            {[
              'Track income & expenses effortlessly',
              'Create custom budgets that work for you',
              'Visual reports & actionable insights',
            ].map((feature, index) => (
              <li key={index} className="flex items-start gap-3">
                <div className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-indigo-500/20">
                  <Check className="h-4 w-4 text-indigo-200" />
                </div>
                <span className="text-indigo-100">{feature}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Form Area */}
      <div className="flex flex-1 flex-col justify-center px-4 py-12 sm:px-6 lg:px-20 xl:px-24">
        {/* Mobile Branding Banner */}
        <div className="mb-8 lg:hidden">
          <div className="flex items-center justify-center gap-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600">
              <Wallet className="h-5 w-5 text-white" />
            </div>
            <h1 className="text-xl font-bold text-slate-900">Budgify</h1>
          </div>
        </div>

        {/* Form Content */}
        <div className="mx-auto w-full max-w-md">{children}</div>
      </div>
    </div>
  );
}
