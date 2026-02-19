import { apiClient } from '../lib/api'
import {
  AccountCategory,
  Account,
  Transaction,
  CreateAccountCategoryRequest,
  UpdateAccountCategoryRequest,
  CreateAccountRequest,
  UpdateAccountRequest,
  CreateTransactionRequest,
  UpdateTransactionRequest,
  ApiSuccessResponse,
  FinancePaginationParams,
} from '../types'

// ===== ACCOUNT CATEGORIES SERVICE =====

export const accountCategoryService = {
  // Get all account categories for tenant
  list: async (params?: FinancePaginationParams): Promise<AccountCategory[]> => {
    const response = await apiClient.get<ApiSuccessResponse<AccountCategory[]>>(
      '/api/finance/categories',
      { params }
    )
    return response.data.data
  },

  // Get single account category
  get: async (categoryId: string): Promise<AccountCategory> => {
    const response = await apiClient.get<ApiSuccessResponse<AccountCategory>>(
      `/api/finance/categories/${categoryId}`
    )
    return response.data.data
  },

  // Create account category
  create: async (request: CreateAccountCategoryRequest): Promise<AccountCategory> => {
    const response = await apiClient.post<ApiSuccessResponse<AccountCategory>>(
      '/api/finance/categories',
      request
    )
    return response.data.data
  },

  // Update account category
  update: async (categoryId: string, request: UpdateAccountCategoryRequest): Promise<AccountCategory> => {
    const response = await apiClient.patch<ApiSuccessResponse<AccountCategory>>(
      `/api/finance/categories/${categoryId}`,
      request
    )
    return response.data.data
  },

  // Delete account category
  delete: async (categoryId: string): Promise<void> => {
    await apiClient.delete(`/api/finance/categories/${categoryId}`)
  },
}

// ===== ACCOUNTS SERVICE =====

export const accountService = {
  // Get all accounts for tenant
  list: async (params?: FinancePaginationParams): Promise<Account[]> => {
    const response = await apiClient.get<ApiSuccessResponse<Account[]>>(
      '/api/finance/accounts',
      { params }
    )
    return response.data.data
  },

  // Get single account
  get: async (accountId: string): Promise<Account> => {
    const response = await apiClient.get<ApiSuccessResponse<Account>>(
      `/api/finance/accounts/${accountId}`
    )
    return response.data.data
  },

  // Create account
  create: async (request: CreateAccountRequest): Promise<Account> => {
    const response = await apiClient.post<ApiSuccessResponse<Account>>(
      '/api/finance/accounts',
      request
    )
    return response.data.data
  },

  // Update account
  update: async (accountId: string, request: UpdateAccountRequest): Promise<Account> => {
    const response = await apiClient.patch<ApiSuccessResponse<Account>>(
      `/api/finance/accounts/${accountId}`,
      request
    )
    return response.data.data
  },

  // Delete account
  delete: async (accountId: string): Promise<void> => {
    await apiClient.delete(`/api/finance/accounts/${accountId}`)
  },
}

// ===== TRANSACTIONS SERVICE =====

export const transactionService = {
  // Get all transactions for tenant
  list: async (params?: FinancePaginationParams): Promise<Transaction[]> => {
    const response = await apiClient.get<ApiSuccessResponse<Transaction[]>>(
      '/api/finance/transactions',
      { params }
    )
    return response.data.data
  },

  // Get transactions for specific account
  listByAccount: async (accountId: string, params?: FinancePaginationParams): Promise<Transaction[]> => {
    const response = await apiClient.get<ApiSuccessResponse<Transaction[]>>(
      `/api/finance/accounts/${accountId}/transactions`,
      { params }
    )
    return response.data.data
  },

  // Get single transaction
  get: async (transactionId: string): Promise<Transaction> => {
    const response = await apiClient.get<ApiSuccessResponse<Transaction>>(
      `/api/finance/transactions/${transactionId}`
    )
    return response.data.data
  },

  // Create transaction
  create: async (request: CreateTransactionRequest): Promise<Transaction> => {
    const response = await apiClient.post<ApiSuccessResponse<Transaction>>(
      '/api/finance/transactions',
      request
    )
    return response.data.data
  },

  // Update transaction
  update: async (transactionId: string, request: UpdateTransactionRequest): Promise<Transaction> => {
    const response = await apiClient.patch<ApiSuccessResponse<Transaction>>(
      `/api/finance/transactions/${transactionId}`,
      request
    )
    return response.data.data
  },

  // Delete transaction
  delete: async (transactionId: string): Promise<void> => {
    await apiClient.delete(`/api/finance/transactions/${transactionId}`)
  },
}
