import React, { useEffect, useState } from 'react'
import { Account, AccountCategory, CreateAccountRequest, UpdateAccountRequest } from '../../types'
import { accountService, accountCategoryService } from '../../services/finance.service'

interface AccountFormProps {
  account?: Account
  onSuccess: (account: Account) => void
  onCancel: () => void
  isLoading?: boolean
}

// Form component for creating and editing accounts
export const AccountForm: React.FC<AccountFormProps> = ({
  account,
  onSuccess,
  onCancel,
  isLoading = false,
}) => {
  const [name, setName] = useState(account?.name || '')
  const [description, setDescription] = useState(account?.description || '')
  const [categoryId, setCategoryId] = useState(account?.category_id || '')
  const [type, setType] = useState<'INCOME' | 'EXPENSE'>(account?.type || 'EXPENSE')
  const [categories, setCategories] = useState<AccountCategory[]>([])
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [loadingCategories, setLoadingCategories] = useState(true)

  useEffect(() => {
    loadCategories()
  }, [])

  const loadCategories = async () => {
    try {
      setLoadingCategories(true)
      const data = await accountCategoryService.list()
      setCategories(data.filter((c) => c.is_active))
      if (!categoryId && data.length > 0) {
        setCategoryId(data[0].category_id)
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error al cargar categorías'
      setError(message)
    } finally {
      setLoadingCategories(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsSubmitting(true)

    try {
      if (!name.trim()) {
        setError('Account name is required')
        return
      }

      if (!categoryId) {
        setError('You must select a category')
        return
      }

      let result: Account

      if (account) {
        const updateRequest: UpdateAccountRequest = {
          name: name.trim(),
          description: description.trim() || undefined,
          category_id: categoryId,
          type,
        }
        result = await accountService.update(account.account_id, updateRequest)
      } else {
        const createRequest: CreateAccountRequest = {
          name: name.trim(),
          description: description.trim() || undefined,
          category_id: categoryId,
          type,
        }
        result = await accountService.create(createRequest)
      }

      onSuccess(result)
      setName('')
      setDescription('')
      setCategoryId('')
      setType('EXPENSE')
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error saving account'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
      <h3 className="text-lg font-semibold">
        {account ? 'Edit Account' : 'New Account'}
      </h3>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded p-3 text-red-700 text-sm">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
          Name *
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g., Checking Account, Credit Card..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          disabled={isSubmitting || isLoading}
        />
      </div>

      <div>
        <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
          Category *
        </label>
        <select
          id="category"
          value={categoryId}
          onChange={(e) => setCategoryId(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          disabled={isSubmitting || isLoading || loadingCategories}
        >
          <option value="">Select a category</option>
          {categories.map((cat) => (
            <option key={cat.category_id} value={cat.category_id}>
              {cat.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="type" className="block text-sm font-medium text-gray-700 mb-1">
          Type *
        </label>
        <select
          id="type"
          value={type}
          onChange={(e) => setType(e.target.value as 'INCOME' | 'EXPENSE')}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          disabled={isSubmitting || isLoading}
        >
          <option value="INCOME">Income</option>
          <option value="EXPENSE">Expenses</option>
        </select>
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Optional description..."
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          disabled={isSubmitting || isLoading}
        />
      </div>

      <div className="flex gap-3 justify-end pt-4 border-t">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50"
          disabled={isSubmitting || isLoading}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-blue-400"
          disabled={isSubmitting || isLoading || loadingCategories}
        >
          {isSubmitting ? 'Saving...' : account ? 'Update' : 'Create'}
        </button>
      </div>
    </form>
  )
}
