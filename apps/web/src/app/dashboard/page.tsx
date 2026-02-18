'use client';

import { getSession } from '@/lib/auth/session';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PageHeader } from '@/components/layout/page-header';
import {
  TrendingUp,
  TrendingDown,
  Wallet,
  PieChart,
  Activity,
  Plus,
  Minus,
  BarChart3,
} from 'lucide-react';

export default function DashboardPage() {
  const session = getSession();

  const stats = [
    {
      title: 'Total Income',
      value: '$0.00',
      icon: TrendingUp,
      colorClass: 'text-green-600',
      bgClass: 'bg-green-50',
    },
    {
      title: 'Total Expenses',
      value: '$0.00',
      icon: TrendingDown,
      colorClass: 'text-red-600',
      bgClass: 'bg-red-50',
    },
    {
      title: 'Balance',
      value: '$0.00',
      icon: Wallet,
      colorClass: 'text-blue-600',
      bgClass: 'bg-blue-50',
    },
    {
      title: 'Active Budgets',
      value: '0',
      icon: PieChart,
      colorClass: 'text-purple-600',
      bgClass: 'bg-purple-50',
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Dashboard"
        subtitle={`Welcome back, ${session?.username}!`}
      />

      {/* Stat Cards */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title} className="transition-shadow hover:shadow-md">
            <CardContent className="p-6">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">{stat.title}</p>
                  <p className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
                    {stat.value}
                  </p>
                </div>
                <div className={`rounded-full p-3 ${stat.bgClass}`}>
                  <stat.icon className={`h-6 w-6 ${stat.colorClass}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Your latest transactions and updates</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="mb-4 rounded-full bg-slate-100 p-4">
                <Activity className="h-8 w-8 text-slate-400" />
              </div>
              <p className="text-base font-medium text-slate-900">No Recent Activity</p>
              <p className="mt-2 text-sm text-slate-500">
                Start tracking your finances to see activity here
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Common tasks to get you started</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button variant="outline" className="w-full justify-start" disabled>
              <Plus className="mr-2 h-5 w-5" />
              Add Income
            </Button>
            <Button variant="outline" className="w-full justify-start" disabled>
              <Minus className="mr-2 h-5 w-5" />
              Add Expense
            </Button>
            <Button variant="outline" className="w-full justify-start" disabled>
              <BarChart3 className="mr-2 h-5 w-5" />
              View Reports
            </Button>
            <p className="pt-2 text-xs text-slate-500">
              These features will be available in upcoming releases
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
