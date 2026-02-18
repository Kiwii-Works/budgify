'use client';

import { useState } from 'react';
import { Sidebar } from './sidebar';
import { Topbar } from './topbar';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen">
      {/* Sidebar */}
      <Sidebar
        isMobileOpen={isMobileMenuOpen}
        onClose={() => setIsMobileMenuOpen(false)}
      />

      {/* Main content area */}
      <div className="lg:pl-64">
        {/* Topbar */}
        <Topbar onMenuClick={() => setIsMobileMenuOpen(true)} />

        {/* Page content with constrained width */}
        <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
          {children}
        </main>
      </div>
    </div>
  );
}
