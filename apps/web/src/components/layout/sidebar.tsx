'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Settings, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { ROUTES } from '@/lib/config/constants';
import type { NavItem } from '@/types';

const navItems: NavItem[] = [
  { name: 'Dashboard', href: ROUTES.DASHBOARD, icon: LayoutDashboard },
  { name: 'Settings', href: ROUTES.DASHBOARD_SETTINGS, icon: Settings },
];

interface SidebarProps {
  isMobileOpen: boolean;
  onClose: () => void;
}

export function Sidebar({ isMobileOpen, onClose }: SidebarProps) {
  const pathname = usePathname();

  return (
    <>
      {/* Mobile overlay */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-50 w-64 transform bg-slate-900 text-slate-50 transition-transform duration-300 ease-in-out lg:translate-x-0',
          isMobileOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex h-full flex-col">
          {/* Logo/Header */}
          <div className="flex h-16 items-center justify-between border-b border-slate-800 px-6">
            <h1 className="text-xl font-bold">Budgify</h1>
            <button
              onClick={onClose}
              className="lg:hidden"
              aria-label="Close sidebar"
            >
              <X className="h-6 w-6" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-3 py-4">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              const Icon = item.icon;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={onClose}
                  className={cn(
                    'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-slate-800 text-white'
                      : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'
                  )}
                >
                  {Icon && <Icon className="h-5 w-5" />}
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* Footer (optional) */}
          <div className="border-t border-slate-800 p-4">
            <p className="text-xs text-slate-400">© 2024 Budgify</p>
          </div>
        </div>
      </aside>
    </>
  );
}
