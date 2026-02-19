import React, { useEffect, useState } from 'react'
import { Account, CreateTransactionRequest, UpdateTransactionRequest, Transaction } from '../../types'
import { accountService, transactionService } from '../../services/finance.service'

interface TransactionFormProps {
  transaction?: Transaction
  onSuccess: (transaction: Transaction) => void
  onCancel: () => void
  isLoading?: boolean
}

// Form component for creating and editing transactions
export const TransactionForm: React.FC<TransactionFormProps> = ({
  transaction,
  onSuccess,
  onCancel,
  isLoading = false,
}) => {
  const [accountId, setAccountId] = useState(transaction?.account_id || '')
  const [amount, setAmount] = useState(transaction?.amount.toString() || '')
  const [currency, setCurrency] = useState(transaction?.currency || 'CAD')
  const [occurredOn, setOccurredOn] = useState(transaction?.occurred_on || '')
  const [notes, setNotes] = useState(transaction?.notes || '')
  const [accounts, setAccounts] = useState<Account[]>([])
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [loadingAccounts, setLoadingAccounts] = useState(true)

  useEffect(() => {
    loadAccounts()
  }, [])

  const loadAccounts = async () => {
    try {
      setLoadingAccounts(true)
      const data = await accountService.list()
      setAccounts(data.filter((a) => a.is_active))
      if (!accountId && data.length > 0) {
        setAccountId(data[0].account_id)
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error al cargar cuentas'
      setError(message)
    } finally {
      setLoadingAccounts(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsSubmitting(true)

    try {
      if (!accountId) {
        setError('You must select an account')
        return
      }

      if (!amount || isNaN(parseFloat(amount)) || parseFloat(amount) <= 0) {
        setError('Amount must be greater than 0')
        return
      }

      if (!occurredOn) {
        setError('Date is required')
        return
      }

      let result: Transaction

      if (transaction) {
        const updateRequest: UpdateTransactionRequest = {
          account_id: accountId,
          amount: parseFloat(amount),
          currency,
          occurred_on: occurredOn,
          notes: notes.trim() || undefined,
        }
        result = await transactionService.update(transaction.transaction_id, updateRequest)
      } else {
        const createRequest: CreateTransactionRequest = {
          account_id: accountId,
          amount: parseFloat(amount),
          currency,
          occurred_on: occurredOn,
          notes: notes.trim() || undefined,
        }
        result = await transactionService.create(createRequest)
      }

      onSuccess(result)
      setAccountId('')
      setAmount('')
      setCurrency('CAD')
      setOccurredOn('')
      setNotes('')
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error saving transaction'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Get today's date in YYYY-MM-DD format
  const today = new Date().toISOString().split('T')[0]

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
      <h3 className="text-lg font-semibold">
        {transaction ? 'Edit Transaction' : 'New Transaction'}
      </h3>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded p-3 text-red-700 text-sm">
          {error}
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="account" className="block text-sm font-medium text-gray-700 mb-1">
            Account *
          </label>
          <select
            id="account"
            value={accountId}
            onChange={(e) => setAccountId(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            disabled={isSubmitting || isLoading || loadingAccounts}
          >
            <option value="">Select an account</option>
            {accounts.map((acc) => (
              <option key={acc.account_id} value={acc.account_id}>
                {acc.name} ({acc.type === 'INCOME' ? 'Income' : 'Expenses'})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-1">
            Amount *
          </label>
          <div className="flex gap-2">
            <input
              id="amount"
              type="number"
              step="0.01"
              min="0"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="0.00"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              disabled={isSubmitting || isLoading}
            />
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              disabled={isSubmitting || isLoading}
            >
              <option value="CAD">CAD</option>
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
              <option value="MXN">MXN</option>
            </select>
          </div>
        </div>
      </div>

      <div>
        <label htmlFor="occurredOn" className="block text-sm font-medium text-gray-700 mb-1">
          Date *
        </label>
        <input
          id="occurredOn"
          type="date"
          value={occurredOn}
          onChange={(e) => setOccurredOn(e.target.value)}
          max={today}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          disabled={isSubmitting || isLoading}
        />
      </div>

      <div>
        <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-1">
          Notes
        </label>
        <textarea
          id="notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Additional transaction notes..."
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
          disabled={isSubmitting || isLoading || loadingAccounts}
        >
          {isSubmitting ? 'Saving...' : transaction ? 'Update' : 'Create'}
        </button>
      </div>
    </form>
  )
}
