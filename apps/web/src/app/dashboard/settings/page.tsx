'use client';

import { getSession } from '@/lib/auth/session';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { PageHeader } from '@/components/layout/page-header';
import { User, Lock, Bell, AlertTriangle } from 'lucide-react';

export default function SettingsPage() {
  const session = getSession();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Settings update functionality will be implemented later
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Settings"
        subtitle="Manage your account settings and preferences"
      />

      <div className="grid gap-6">
        {/* Profile Information */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <User className="h-5 w-5 text-slate-500" />
              <CardTitle>Profile Information</CardTitle>
            </div>
            <CardDescription>
              Update your personal details and profile information
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="space-y-2">
                <Label htmlFor="username" className="text-sm font-medium">
                  Username
                </Label>
                <Input
                  id="username"
                  defaultValue={session?.username}
                  disabled
                />
                <p className="text-xs text-slate-500">
                  Your unique username across the platform
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="email" className="text-sm font-medium">
                  Email Address
                </Label>
                <Input
                  id="email"
                  type="email"
                  defaultValue={session?.email}
                  disabled
                />
                <p className="text-xs text-slate-500">
                  Your email for notifications and account recovery
                </p>
              </div>

              <Button type="submit" disabled>
                Save Changes (Coming Soon)
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Account Settings */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Lock className="h-5 w-5 text-slate-500" />
              <CardTitle>Account Settings</CardTitle>
            </div>
            <CardDescription>
              Manage your password and security preferences
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            <div>
              <h4 className="mb-2 text-sm font-medium text-slate-900">Password</h4>
              <p className="mb-4 text-sm text-slate-600">
                Change your password to keep your account secure
              </p>
              <Button variant="outline" disabled>
                Change Password (Phase 2)
              </Button>
            </div>

            <div className="border-t pt-5">
              <h4 className="mb-2 text-sm font-medium text-slate-900">
                Two-Factor Authentication
              </h4>
              <p className="mb-4 text-sm text-slate-600">
                Add an extra layer of security to your account
              </p>
              <div className="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 p-4">
                <span className="text-sm font-medium text-slate-700">Enable 2FA</span>
                <div className="h-6 w-11 rounded-full bg-slate-300"></div>
              </div>
              <p className="mt-2 text-xs text-slate-500">Coming in Phase 2</p>
            </div>
          </CardContent>
        </Card>

        {/* Preferences */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Bell className="h-5 w-5 text-slate-500" />
              <CardTitle>Preferences</CardTitle>
            </div>
            <CardDescription>
              Customize your experience and notification settings
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            <div>
              <h4 className="mb-4 text-sm font-medium text-slate-900">
                Notifications
              </h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 p-4">
                  <div>
                    <p className="text-sm font-medium text-slate-700">
                      Email Notifications
                    </p>
                    <p className="text-xs text-slate-500">
                      Receive updates via email
                    </p>
                  </div>
                  <div className="h-6 w-11 rounded-full bg-slate-300"></div>
                </div>

                <div className="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 p-4">
                  <div>
                    <p className="text-sm font-medium text-slate-700">
                      Budget Alerts
                    </p>
                    <p className="text-xs text-slate-500">
                      Get notified when approaching budget limits
                    </p>
                  </div>
                  <div className="h-6 w-11 rounded-full bg-slate-300"></div>
                </div>
              </div>
              <p className="mt-3 text-xs text-slate-500">Coming in Phase 2</p>
            </div>
          </CardContent>
        </Card>

        {/* Danger Zone */}
        <Card className="border-red-200">
          <CardHeader>
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-red-500" />
              <CardTitle className="text-red-700">Danger Zone</CardTitle>
            </div>
            <CardDescription>
              Irreversible actions that affect your account
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg border border-red-200 bg-red-50 p-4">
              <h4 className="mb-2 text-sm font-medium text-red-900">
                Delete Account
              </h4>
              <p className="mb-4 text-sm text-red-700">
                Permanently delete your account and all associated data. This action
                cannot be undone.
              </p>
              <Button variant="outline" className="border-red-300 text-red-700 hover:bg-red-100" disabled>
                Delete Account (Phase 2)
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
