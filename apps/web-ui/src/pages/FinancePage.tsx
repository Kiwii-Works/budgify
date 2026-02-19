import React, { useState } from 'react'
import { AccountCategory, Account, Transaction } from '../types'
import { DashboardLayout } from '../components/layout/DashboardLayout'
import { CategoryForm } from '../components/finance/CategoryForm'
import { CategoriesList } from '../components/finance/CategoriesList'
import { AccountForm } from '../components/finance/AccountForm'
import { AccountsList } from '../components/finance/AccountsList'
import { TransactionForm } from '../components/finance/TransactionForm'
import { TransactionsList } from '../components/finance/TransactionsList'

type Tab = 'categories' | 'accounts' | 'transactions'

// Main Finance page component for managing financial data
const FinancePage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>('categories')
  const [refreshKey, setRefreshKey] = useState(0)

  // Categories state
  const [showCategoryForm, setShowCategoryForm] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState<AccountCategory | undefined>()

  // Accounts state
  const [showAccountForm, setShowAccountForm] = useState(false)
  const [selectedAccount, setSelectedAccount] = useState<Account | undefined>()

  // Transactions state
  const [showTransactionForm, setShowTransactionForm] = useState(false)
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | undefined>()

  // Category handlers
  const handleEditCategory = (category: AccountCategory) => {
    setSelectedCategory(category)
    setShowCategoryForm(true)
  }

  const handleCategorySuccess = () => {
    setShowCategoryForm(false)
    setSelectedCategory(undefined)
    setRefreshKey((k) => k + 1)
  }

  // Account handlers
  const handleEditAccount = (account: Account) => {
    setSelectedAccount(account)
    setShowAccountForm(true)
  }

  const handleAccountSuccess = () => {
    setShowAccountForm(false)
    setSelectedAccount(undefined)
    setRefreshKey((k) => k + 1)
  }

  // Transaction handlers
  const handleEditTransaction = (transaction: Transaction) => {
    setSelectedTransaction(transaction)
    setShowTransactionForm(true)
  }

  const handleTransactionSuccess = () => {
    setShowTransactionForm(false)
    setSelectedTransaction(undefined)
    setRefreshKey((k) => k + 1)
  }

  return (
    <DashboardLayout title="Finance Management">
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Finance Management</h1>
            <p className="mt-2 text-gray-600">Manage your categories, accounts and financial transactions</p>
          </div>

          {/* Tabs */}
          <div className="mb-6 border-b border-gray-200">
            <nav className="flex gap-8" aria-label="Tabs">
              <button
                onClick={() => setActiveTab('categories')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'categories'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Categories
              </button>
              <button
                onClick={() => setActiveTab('accounts')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'accounts'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Accounts
              </button>
              <button
                onClick={() => setActiveTab('transactions')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'transactions'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Transactions
              </button>
            </nav>
          </div>

          {/* Categories Tab */}
          {activeTab === 'categories' && (
            <div className="space-y-6">
              {showCategoryForm ? (
                <CategoryForm
                  category={selectedCategory}
                  onSuccess={handleCategorySuccess}
                  onCancel={() => {
                    setShowCategoryForm(false)
                    setSelectedCategory(undefined)
                  }}
                />
              ) : (
                <button
                  onClick={() => setShowCategoryForm(true)}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
                >
                  + New Category
                </button>
              )}
              <CategoriesList
                key={refreshKey}
                onEdit={handleEditCategory}
                onRefresh={() => setRefreshKey((k) => k + 1)}
                isLoading={showCategoryForm}
              />
            </div>
          )}

          {/* Accounts Tab */}
          {activeTab === 'accounts' && (
            <div className="space-y-6">
              {showAccountForm ? (
                <AccountForm
                  account={selectedAccount}
                  onSuccess={handleAccountSuccess}
                  onCancel={() => {
                    setShowAccountForm(false)
                    setSelectedAccount(undefined)
                  }}
                />
              ) : (
                <button
                  onClick={() => setShowAccountForm(true)}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
                >
                  + New Account
                </button>
              )}
              <AccountsList
                key={refreshKey}
                onEdit={handleEditAccount}
                onRefresh={() => setRefreshKey((k) => k + 1)}
                isLoading={showAccountForm}
              />
            </div>
          )}

          {/* Transactions Tab */}
          {activeTab === 'transactions' && (
            <div className="space-y-6">
              {showTransactionForm ? (
                <TransactionForm
                  transaction={selectedTransaction}
                  onSuccess={handleTransactionSuccess}
                  onCancel={() => {
                    setShowTransactionForm(false)
                    setSelectedTransaction(undefined)
                  }}
                />
              ) : (
                <button
                  onClick={() => setShowTransactionForm(true)}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
                >
                  + New Transaction
                </button>
              )}
              <TransactionsList
                key={refreshKey}
                onEdit={handleEditTransaction}
                onRefresh={() => setRefreshKey((k) => k + 1)}
                isLoading={showTransactionForm}
              />
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  )
}

export default FinancePage
