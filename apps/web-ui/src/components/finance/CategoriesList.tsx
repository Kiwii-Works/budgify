import React, { useEffect, useState } from 'react'
import { AccountCategory } from '../../types'
import { accountCategoryService } from '../../services/finance.service'

interface CategoriesListProps {
  onEdit: (category: AccountCategory) => void
  onRefresh?: () => void
  isLoading?: boolean
}

// List component for displaying account categories with CRUD operations
export const CategoriesList: React.FC<CategoriesListProps> = ({
  onEdit,
  onRefresh,
  isLoading = false,
}) => {
  const [categories, setCategories] = useState<AccountCategory[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deleting, setDeleting] = useState<string | null>(null)

  useEffect(() => {
    loadCategories()
  }, [])

  const loadCategories = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await accountCategoryService.list()
      setCategories(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error loading categories'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (categoryId: string) => {
    if (!confirm('Are you sure you want to delete this category?')) return

    try {
      setDeleting(categoryId)
      await accountCategoryService.delete(categoryId)
      setCategories(categories.filter((c) => c.category_id !== categoryId))
      onRefresh?.()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error deleting category'
      setError(message)
    } finally {
      setDeleting(null)
    }
  }

  const handleToggleActive = async (category: AccountCategory) => {
    try {
      const updated = await accountCategoryService.update(category.category_id, {
        is_active: !category.is_active,
      })
      setCategories(
        categories.map((c) => (c.category_id === updated.category_id ? updated : c))
      )
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error updating category'
      setError(message)
    }
  }

  if (loading || isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-center items-center h-32">
          <div className="text-gray-500">Loading categories...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="bg-red-50 border border-red-200 rounded p-3 text-red-700">
          {error}
        </div>
        <button
          onClick={loadCategories}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    )
  }

  if (categories.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center text-gray-500 py-12">
          No categories. Create one to start.
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-50 border-b">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              Name
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              Description
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              Status
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="divide-y">
          {categories.map((category) => (
            <tr key={category.category_id} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm font-medium text-gray-900">{category.name}</div>
              </td>
              <td className="px-6 py-4">
                <div className="text-sm text-gray-500 max-w-xs truncate">
                  {category.description || '-'}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <button
                  onClick={() => handleToggleActive(category)}
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium cursor-pointer ${
                    category.is_active
                      ? 'bg-green-100 text-green-800 hover:bg-green-200'
                      : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                  }`}
                >
                  {category.is_active ? 'Active' : 'Inactive'}
                </button>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right space-x-2">
                <button
                  onClick={() => onEdit(category)}
                  className="text-blue-600 hover:text-blue-900 text-sm font-medium"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(category.category_id)}
                  disabled={deleting === category.category_id}
                  className="text-red-600 hover:text-red-900 text-sm font-medium disabled:opacity-50"
                >
                  {deleting === category.category_id ? 'Deleting...' : 'Delete'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
