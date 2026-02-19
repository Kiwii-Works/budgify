import React, { useState } from 'react'
import { AccountCategory, CreateAccountCategoryRequest, UpdateAccountCategoryRequest } from '../../types'
import { accountCategoryService } from '../../services/finance.service'

interface CategoryFormProps {
  category?: AccountCategory
  onSuccess: (category: AccountCategory) => void
  onCancel: () => void
  isLoading?: boolean
}

// Form component for creating and editing account categories
export const CategoryForm: React.FC<CategoryFormProps> = ({
  category,
  onSuccess,
  onCancel,
  isLoading = false,
}) => {
  const [name, setName] = useState(category?.name || '')
  const [description, setDescription] = useState(category?.description || '')
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsSubmitting(true)

    try {
      if (!name.trim()) {
        setError('Category name is required')
        return
      }

      let result: AccountCategory

      if (category) {
        const updateRequest: UpdateAccountCategoryRequest = {
          name: name.trim(),
          description: description.trim() || undefined,
        }
        result = await accountCategoryService.update(category.category_id, updateRequest)
      } else {
        const createRequest: CreateAccountCategoryRequest = {
          name: name.trim(),
          description: description.trim() || undefined,
        }
        result = await accountCategoryService.create(createRequest)
      }

      onSuccess(result)
      setName('')
      setDescription('')
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error saving category'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
      <h3 className="text-lg font-semibold">
        {category ? 'Edit Category' : 'New Category'}
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
          placeholder="e.g., Personal expenses, Income..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          disabled={isSubmitting || isLoading}
        />
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
          disabled={isSubmitting || isLoading}
        >
          {isSubmitting ? 'Saving...' : category ? 'Update' : 'Create'}
        </button>
      </div>
    </form>
  )
}
