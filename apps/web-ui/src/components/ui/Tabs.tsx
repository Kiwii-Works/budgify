import React from 'react'

interface TabsProps {
  tabs: Array<{ label: string; value: string; content: React.ReactNode }>
  defaultValue?: string
  onChange?: (value: string) => void
}

// Tab navigation component for switching between content sections
export const Tabs: React.FC<TabsProps> = ({ tabs, defaultValue, onChange }) => {
  // Track which tab is currently active
  const [activeTab, setActiveTab] = React.useState(defaultValue || tabs[0].value)

  const handleTabChange = (value: string) => {
    setActiveTab(value)
    onChange?.(value)
  }

  return (
    <div>
      {/* Tab navigation buttons */}
      <div className="flex border-b border-slate-200">
        {tabs.map((tab) => (
          <button
            key={tab.value}
            onClick={() => handleTabChange(tab.value)}
            className={`px-4 py-2 font-medium text-sm transition-colors ${
              activeTab === tab.value
                ? 'text-primary-600 border-b-2 border-primary-600 -mb-px'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {/* Tab content */}
      <div className="mt-4">
        {tabs.find((tab) => tab.value === activeTab)?.content}
      </div>
    </div>
  )
}
