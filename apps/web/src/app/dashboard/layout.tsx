'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth/session';
import { ROUTES } from '@/lib/config/constants';
import { DashboardLayout } from '@/components/layout/dashboard-layout';

export default function DashboardLayoutWrapper({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();

  useEffect(() => {
    // Client-side route protection
    if (!isAuthenticated()) {
      router.push(ROUTES.LOGIN);
    }
  }, [router]);

  // Don't render children until auth check is complete
  if (!isAuthenticated()) {
    return null;
  }

  return <DashboardLayout>{children}</DashboardLayout>;
}
