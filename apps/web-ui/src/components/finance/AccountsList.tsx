import React, { useEffect, useState } from 'react'
import { Account, AccountCategory } from '../../types'
import { accountService, accountCategoryService } from '../../services/finance.service'

interface AccountsListProps {
  onEdit: (account: Account) => void
  onRefresh?: () => void
  isLoading?: boolean
}

// List component for displaying accounts with filtering by type and CRUD operations
export const AccountsList: React.FC<AccountsListProps> = ({
  onEdit,
  onRefresh,
  isLoading = false,
}) => {
  const [accounts, setAccounts] = useState<Account[]>([])
  const [categories, setCategories] = useState<Map<string, AccountCategory>>(new Map())
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deleting, setDeleting] = useState<string | null>(null)
  const [filterType, setFilterType] = useState<'ALL' | 'INCOME' | 'EXPENSE'>('ALL')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)

      const [accountsData, categoriesData] = await Promise.all([
        accountService.list(),
        accountCategoryService.list(),
      ])

      setAccounts(accountsData)

      const categoryMap = new Map<string, AccountCategory>()
      categoriesData.forEach((cat) => {
        categoryMap.set(cat.category_id, cat)
      })
      setCategories(categoryMap)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error loading accounts'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (accountId: string) => {
    if (!confirm('¿Estás seguro de que deseas eliminar esta cuenta?')) return

    try {
      setDeleting(accountId)
      await accountService.delete(accountId)
      setAccounts(accounts.filter((a) => a.account_id !== accountId))
      onRefresh?.()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error deleting account'
      setError(message)
    } finally {
      setDeleting(null)
    }
  }

  const handleToggleActive = async (account: Account) => {
    try {
      const updated = await accountService.update(account.account_id, {
        is_active: !account.is_active,
      })
      setAccounts(
        accounts.map((a) => (a.account_id === updated.account_id ? updated : a))
      )
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error updating account'
      setError(message)
    }
  }

  const filteredAccounts =
    filterType === 'ALL'
      ? accounts
      : accounts.filter((a) => a.type === filterType)

  if (loading || isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-center items-center h-32">
          <div className="text-gray-500">Loading accounts...</div>
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
          onClick={loadData}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    )
  }

  if (accounts.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center text-gray-500 py-12">
          No accounts. Create one to start.
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 border-b bg-gray-50 flex justify-between items-center">
        <div className="flex gap-2">
          <button
            onClick={() => setFilterType('ALL')}
            className={`px-3 py-1 rounded text-sm font-medium ${
              filterType === 'ALL'
                ? 'bg-blue-600 text-white'
                : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            All ({accounts.length})
          </button>
          <button
            onClick={() => setFilterType('INCOME')}
            className={`px-3 py-1 rounded text-sm font-medium ${
              filterType === 'INCOME'
                ? 'bg-green-600 text-white'
                : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            Income ({accounts.filter((a) => a.type === 'INCOME').length})
          </button>
          <button
            onClick={() => setFilterType('EXPENSE')}
            className={`px-3 py-1 rounded text-sm font-medium ${
              filterType === 'EXPENSE'
                ? 'bg-red-600 text-white'
                : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            Expenses ({accounts.filter((a) => a.type === 'EXPENSE').length})
          </button>
        </div>
      </div>

      <table className="w-full">
        <thead className="bg-gray-50 border-b">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              Name
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              Category
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              Type
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
          {filteredAccounts.map((account) => {
            const category = categories.get(account.category_id)
            return (
              <tr key={account.account_id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">{account.name}</div>
                  <div className="text-sm text-gray-500">{account.description}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-600">{category?.name || 'N/A'}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      account.type === 'INCOME'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {account.type === 'INCOME' ? 'Income' : 'Expenses'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <button
                    onClick={() => handleToggleActive(account)}
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium cursor-pointer ${
                      account.is_active
                        ? 'bg-green-100 text-green-800 hover:bg-green-200'
                        : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                    }`}
                  >
                    {account.is_active ? 'Active' : 'Inactive'}
                  </button>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right space-x-2">
                  <button
                    onClick={() => onEdit(account)}
                    className="text-blue-600 hover:text-blue-900 text-sm font-medium"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(account.account_id)}
                    disabled={deleting === account.account_id}
                    className="text-red-600 hover:text-red-900 text-sm font-medium disabled:opacity-50"
                  >
                    {deleting === account.account_id ? 'Deleting...' : 'Delete'}
                  </button>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
