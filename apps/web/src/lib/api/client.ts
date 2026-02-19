/**
 * API client with JWT Bearer token support and automatic refresh handling.
 */

import axios, { AxiosInstance, AxiosError, AxiosResponse } from 'axios';
import { API_URL } from '@/lib/config/constants';
import type { ApiError, ApiResponse } from './types';

let accessToken: string | null = null;

/**
 * Create axios instance with withCredentials for automatic cookie handling
 */
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Token management functions
 */
export function getAccessToken(): string | null {
  return accessToken;
}

export function setAccessToken(token: string | null): void {
  accessToken = token;
}

export function clearTokens(): void {
  accessToken = null;
}

/**
 * Request interceptor: Inject Bearer token into Authorization header
 */
apiClient.interceptors.request.use(
  (config) => {
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor: Handle 401 responses and attempt token refresh
 */
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;

    // Handle 401 Unauthorized responses
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (accessToken) {
        try {
          // Attempt to refresh the access token
          const refreshResponse = await axios.post(
            `${API_URL}/api/auth/refresh`,
            {},
            {
              withCredentials: true,
              timeout: 10000,
            }
          );

          // Extract new access token from response
          const newAccessToken = refreshResponse.data.data?.access_token;
          if (newAccessToken) {
            setAccessToken(newAccessToken);

            // Update authorization header and retry original request
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            }

            return apiClient(originalRequest);
          }
        } catch (refreshError) {
          // Refresh failed - clear tokens and reject
          clearTokens();
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

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

/**
 * Handle API responses and convert to standardized format
 */
async function handleResponse<T>(response: AxiosResponse): Promise<ApiResponse<T>> {
  if (response.status >= 200 && response.status < 300) {
    return response.data as ApiResponse<T>;
  }

  const errorData: ApiError = response.data;
  throw new ApiClientError(
    `API Error: ${response.status}`,
    response.status,
    errorData.detail || response.statusText
  );
}

/**
 * Generic API request function
 */
export async function apiRequest<T = unknown>(
  endpoint: string,
  method: 'GET' | 'POST' | 'PATCH' | 'DELETE' = 'GET',
  data?: unknown,
  headers?: Record<string, string>
): Promise<ApiResponse<T>> {
  try {
    const response = await apiClient({
      method,
      url: endpoint,
      data,
      headers,
    });
    return await handleResponse<T>(response);
  } catch (error) {
    if (error instanceof ApiClientError) {
      throw error;
    }

    if (axios.isAxiosError(error)) {
      const status = error.response?.status || 0;
      const errorMessage = error.response?.data?.detail || error.message;
      throw new ApiClientError(`API Error: ${status}`, status, errorMessage);
    }

    throw new ApiClientError(
      'Network error',
      0,
      error instanceof Error ? error.message : 'Unknown error'
    );
  }
}

/**
 * Convenience methods for common HTTP verbs
 */
export const api = {
  get: <T = unknown>(endpoint: string, headers?: Record<string, string>) =>
    apiRequest<T>(endpoint, 'GET', undefined, headers),

  post: <T = unknown>(
    endpoint: string,
    body?: unknown,
    headers?: Record<string, string>
  ) =>
    apiRequest<T>(endpoint, 'POST', body, headers),

  patch: <T = unknown>(
    endpoint: string,
    body?: unknown,
    headers?: Record<string, string>
  ) =>
    apiRequest<T>(endpoint, 'PATCH', body, headers),

  delete: <T = unknown>(endpoint: string, headers?: Record<string, string>) =>
    apiRequest<T>(endpoint, 'DELETE', undefined, headers),
};
