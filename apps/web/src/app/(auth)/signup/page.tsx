'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import Link from 'next/link';
import { toast } from 'sonner';
import { Key, User, Mail, Phone, Lock, Loader2 } from 'lucide-react';
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
import { api, ApiClientError } from '@/lib/api/client';
import { setSession } from '@/lib/auth/session';
import { ROUTES } from '@/lib/config/constants';
import type { RegisterRequest, RegisterResponse } from '@/lib/api/types';

const signupSchema = z.object({
  tenant_id: z.string().uuid('Invalid tenant ID format'),
  username: z.string().min(3, 'Username must be at least 3 characters').max(30),
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  email: z.string().email('Invalid email address'),
  phone_number: z.string().min(10, 'Phone number must be at least 10 digits'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type SignupFormData = z.infer<typeof signupSchema>;

export default function SignupPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
  });

  const onSubmit = async (data: SignupFormData) => {
    setIsLoading(true);

    try {
      const { tenant_id, ...registerData } = data;

      const response = await api.post<RegisterResponse>(
        '/api/auth/register',
        registerData,
        {
          'X-Tenant-Id': tenant_id,
        }
      );

      // Store session
      setSession({
        userId: response.data.user_id,
        tenantId: tenant_id,
        username: response.data.username,
        email: response.data.email,
      });

      toast.success('Account created successfully!');
      router.push(ROUTES.DASHBOARD);
    } catch (error) {
      if (error instanceof ApiClientError) {
        toast.error(error.detail || 'Failed to create account');
      } else {
        toast.error('An unexpected error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="shadow-lg">
      <CardHeader className="space-y-1 pb-6">
        <CardTitle className="text-2xl font-bold">Create an account</CardTitle>
        <CardDescription className="text-base">
          Enter your information to get started
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit(onSubmit)}>
        <CardContent className="space-y-5">
          {/* Tenant ID */}
          <div className="space-y-2">
            <Label htmlFor="tenant_id" className="text-sm font-medium">
              Tenant ID
            </Label>
            <div className="relative">
              <Key className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
              <Input
                id="tenant_id"
                placeholder="00000000-0000-0000-0000-000000000000"
                className="pl-10"
                {...register('tenant_id')}
              />
            </div>
            {errors.tenant_id ? (
              <p className="text-xs text-red-600">{errors.tenant_id.message}</p>
            ) : (
              <p className="text-xs text-slate-500">
                Your organization's tenant ID
              </p>
            )}
          </div>

          {/* Username */}
          <div className="space-y-2">
            <Label htmlFor="username" className="text-sm font-medium">
              Username
            </Label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
              <Input
                id="username"
                placeholder="johndoe"
                className="pl-10"
                {...register('username')}
              />
            </div>
            {errors.username ? (
              <p className="text-xs text-red-600">{errors.username.message}</p>
            ) : (
              <p className="text-xs text-slate-500">
                Choose a unique username (3-30 characters)
              </p>
            )}
          </div>

          {/* Name Fields - Grouped */}
          <div className="grid gap-4 sm:grid-cols-2">
            {/* First Name */}
            <div className="space-y-2">
              <Label htmlFor="first_name" className="text-sm font-medium">
                First Name
              </Label>
              <Input
                id="first_name"
                placeholder="John"
                {...register('first_name')}
              />
              {errors.first_name && (
                <p className="text-xs text-red-600">
                  {errors.first_name.message}
                </p>
              )}
            </div>

            {/* Last Name */}
            <div className="space-y-2">
              <Label htmlFor="last_name" className="text-sm font-medium">
                Last Name
              </Label>
              <Input
                id="last_name"
                placeholder="Doe"
                {...register('last_name')}
              />
              {errors.last_name && (
                <p className="text-xs text-red-600">{errors.last_name.message}</p>
              )}
            </div>
          </div>

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
                {...register('email')}
              />
            </div>
            {errors.email ? (
              <p className="text-xs text-red-600">{errors.email.message}</p>
            ) : (
              <p className="text-xs text-slate-500">
                We'll never share your email
              </p>
            )}
          </div>

          {/* Phone Number */}
          <div className="space-y-2">
            <Label htmlFor="phone_number" className="text-sm font-medium">
              Phone Number
            </Label>
            <div className="relative">
              <Phone className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
              <Input
                id="phone_number"
                placeholder="+1234567890"
                className="pl-10"
                {...register('phone_number')}
              />
            </div>
            {errors.phone_number ? (
              <p className="text-xs text-red-600">
                {errors.phone_number.message}
              </p>
            ) : (
              <p className="text-xs text-slate-500">
                Include country code (e.g., +1)
              </p>
            )}
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
                {...register('password')}
              />
            </div>
            {errors.password ? (
              <p className="text-xs text-red-600">{errors.password.message}</p>
            ) : (
              <p className="text-xs text-slate-500">
                Must be at least 8 characters
              </p>
            )}
          </div>
        </CardContent>

        <CardFooter className="flex flex-col space-y-4 pt-6">
          <Button
            type="submit"
            className="w-full"
            size="lg"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Creating account...
              </>
            ) : (
              'Create account'
            )}
          </Button>
          <p className="text-center text-sm text-slate-600">
            Already have an account?{' '}
            <Link
              href={ROUTES.LOGIN}
              className="font-medium text-indigo-600 transition-colors hover:text-indigo-700 hover:underline"
            >
              Log in
            </Link>
          </p>
        </CardFooter>
      </form>
    </Card>
  );
}
