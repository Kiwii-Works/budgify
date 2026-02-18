'use client';

import { Menu, LogOut, User } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { clearSession, getSession } from '@/lib/auth/session';
import { ROUTES } from '@/lib/config/constants';

interface TopbarProps {
  onMenuClick: () => void;
}

export function Topbar({ onMenuClick }: TopbarProps) {
  const router = useRouter();
  const session = getSession();

  const handleLogout = () => {
    clearSession();
    router.push(ROUTES.LOGIN);
  };

  const getInitials = (username: string) => {
    return username.charAt(0).toUpperCase();
  };

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 shadow-sm sm:px-6">
      {/* Left: Mobile menu button + breadcrumbs */}
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuClick}
          className="rounded-lg p-2 transition-colors hover:bg-slate-100 lg:hidden"
          aria-label="Open menu"
        >
          <Menu className="h-5 w-5 text-slate-700" />
        </button>
        {/* Breadcrumbs placeholder - can be implemented later */}
        <div className="hidden text-sm text-slate-500 lg:block">
          {/* Breadcrumbs will go here in future phases */}
        </div>
      </div>

      {/* Right: User info + logout */}
      <div className="flex items-center gap-3">
        {session && (
          <>
            {/* Avatar placeholder circle */}
            <div className="hidden items-center gap-3 sm:flex">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-100 text-sm font-semibold text-indigo-600">
                {getInitials(session.username)}
              </div>
              <div className="flex flex-col items-start">
                <p className="text-sm font-medium text-slate-900">{session.username}</p>
                <p className="text-xs text-slate-500">{session.email}</p>
              </div>
            </div>

            {/* Mobile avatar only */}
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-100 text-sm font-semibold text-indigo-600 sm:hidden">
              {getInitials(session.username)}
            </div>
          </>
        )}

        <Button
          variant="outline"
          size="sm"
          onClick={handleLogout}
          className="gap-2 border-slate-200 hover:bg-slate-50"
        >
          <LogOut className="h-4 w-4" />
          <span className="hidden sm:inline">Logout</span>
        </Button>
      </div>
    </header>
  );
}
