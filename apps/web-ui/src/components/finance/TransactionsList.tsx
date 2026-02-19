import React, { useEffect, useState } from 'react'
import { Transaction, Account } from '../../types'
import { transactionService, accountService } from '../../services/finance.service'

interface TransactionsListProps {
  onEdit: (transaction: Transaction) => void
  onRefresh?: () => void
  isLoading?: boolean
}

// List component for displaying transactions with filtering and CRUD operations
export const TransactionsList: React.FC<TransactionsListProps> = ({
  onEdit,
  onRefresh,
  isLoading = false,
}) => {
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [accounts, setAccounts] = useState<Map<string, Account>>(new Map())
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deleting, setDeleting] = useState<string | null>(null)
  const [filterDirection, setFilterDirection] = useState<'ALL' | 'INCOME' | 'EXPENSE'>('ALL')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)

      const [transactionsData, accountsData] = await Promise.all([
        transactionService.list(),
        accountService.list(),
      ])

      setTransactions(transactionsData)

      const accountMap = new Map<string, Account>()
      accountsData.forEach((acc) => {
        accountMap.set(acc.account_id, acc)
      })
      setAccounts(accountMap)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error loading transactions'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (transactionId: string) => {
    if (!confirm('¿Estás seguro de que deseas eliminar esta transacción?')) return

    try {
      setDeleting(transactionId)
      await transactionService.delete(transactionId)
      setTransactions(transactions.filter((t) => t.transaction_id !== transactionId))
      onRefresh?.()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error deleting transaction'
      setError(message)
    } finally {
      setDeleting(null)
    }
  }

  const filteredTransactions =
    filterDirection === 'ALL'
      ? transactions
      : transactions.filter((t) => t.direction === filterDirection)

  // Sort by date descending
  const sortedTransactions = [...filteredTransactions].sort(
    (a, b) => new Date(b.occurred_on).getTime() - new Date(a.occurred_on).getTime()
  )

  const formatCurrency = (amount: number, currency: string = 'CAD') => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency,
    }).format(amount)
  }

  const formatDate = (dateStr: string) => {
    try {
      return new Intl.DateTimeFormat('es-MX', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      }).format(new Date(dateStr))
    } catch {
      return dateStr
    }
  }

  if (loading || isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-center items-center h-32">
          <div className="text-gray-500">Loading transactions...</div>
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

  if (transactions.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center text-gray-500 py-12">
          No transactions. Create one to start.
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 border-b bg-gray-50 flex justify-between items-center">
        <div className="flex gap-2">
          <button
            onClick={() => setFilterDirection('ALL')}
            className={`px-3 py-1 rounded text-sm font-medium ${
              filterDirection === 'ALL'
                ? 'bg-blue-600 text-white'
                : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            All ({transactions.length})
          </button>
          <button
            onClick={() => setFilterDirection('INCOME')}
            className={`px-3 py-1 rounded text-sm font-medium ${
              filterDirection === 'INCOME'
                ? 'bg-green-600 text-white'
                : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            Income ({transactions.filter((t) => t.direction === 'INCOME').length})
          </button>
          <button
            onClick={() => setFilterDirection('EXPENSE')}
            className={`px-3 py-1 rounded text-sm font-medium ${
              filterDirection === 'EXPENSE'
                ? 'bg-red-600 text-white'
                : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            Expenses ({transactions.filter((t) => t.direction === 'EXPENSE').length})
          </button>
        </div>
      </div>

      <table className="w-full">
        <thead className="bg-gray-50 border-b">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              Date
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              Account
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              Type
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider">
              Amount
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
              Notes
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="divide-y">
          {sortedTransactions.map((transaction) => {
            const account = accounts.get(transaction.account_id)
            return (
              <tr key={transaction.transaction_id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">{formatDate(transaction.occurred_on)}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">{account?.name || 'N/A'}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      transaction.direction === 'INCOME'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {transaction.direction === 'INCOME' ? 'Income' : 'Expense'}
                  </span>
                </td>
                <td
                  className={`px-6 py-4 whitespace-nowrap text-right text-sm font-medium ${
                    transaction.direction === 'INCOME' ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {transaction.direction === 'INCOME' ? '+' : '-'}
                  {formatCurrency(transaction.amount, transaction.currency)}
                </td>
                <td className="px-6 py-4">
                  <div className="text-sm text-gray-500 max-w-xs truncate">
                    {transaction.notes || '-'}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right space-x-2">
                  <button
                    onClick={() => onEdit(transaction)}
                    className="text-blue-600 hover:text-blue-900 text-sm font-medium"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(transaction.transaction_id)}
                    disabled={deleting === transaction.transaction_id}
                    className="text-red-600 hover:text-red-900 text-sm font-medium disabled:opacity-50"
                  >
                    {deleting === transaction.transaction_id ? 'Deleting...' : 'Delete'}
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
