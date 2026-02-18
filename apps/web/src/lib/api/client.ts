/**
 * API client with fetch wrapper and error handling.
 */

import { API_URL } from '@/lib/config/constants';
import type { ApiError, ApiResponse } from './types';

export class ApiClientError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public detail?: string
  ) {
    super(message);
    this.name = 'ApiClientError';
  }
}

interface FetchOptions extends RequestInit {
  headers?: Record<string, string>;
}

async function handleResponse<T>(response: Response): Promise<ApiResponse<T>> {
  const contentType = response.headers.get('content-type');
  const isJson = contentType?.includes('application/json');

  if (!response.ok) {
    let errorDetail = response.statusText;

    if (isJson) {
      try {
        const errorData: ApiError = await response.json();
        errorDetail = errorData.detail || errorDetail;
      } catch {
        // Ignore JSON parse errors
      }
    }

    throw new ApiClientError(
      `API Error: ${response.status}`,
      response.status,
      errorDetail
    );
  }

  if (isJson) {
    return await response.json();
  }

  throw new ApiClientError('Invalid response format', response.status);
}

export async function apiRequest<T = unknown>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<ApiResponse<T>> {
  const url = `${API_URL}${endpoint}`;

  const defaultHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);
    return await handleResponse<T>(response);
  } catch (error) {
    if (error instanceof ApiClientError) {
      throw error;
    }

    // Network or other errors
    throw new ApiClientError(
      'Network error',
      0,
      error instanceof Error ? error.message : 'Unknown error'
    );
  }
}

// Convenience methods
export const api = {
  get: <T = unknown>(endpoint: string, headers?: Record<string, string>) =>
    apiRequest<T>(endpoint, { method: 'GET', headers }),

  post: <T = unknown>(
    endpoint: string,
    body?: unknown,
    headers?: Record<string, string>
  ) =>
    apiRequest<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
      headers,
    }),

  patch: <T = unknown>(
    endpoint: string,
    body?: unknown,
    headers?: Record<string, string>
  ) =>
    apiRequest<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(body),
      headers,
    }),

  delete: <T = unknown>(endpoint: string, headers?: Record<string, string>) =>
    apiRequest<T>(endpoint, { method: 'DELETE', headers }),
};
