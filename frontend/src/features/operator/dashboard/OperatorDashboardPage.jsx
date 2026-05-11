import { useState } from 'react'
import { useOperatorOverviewQuery } from '../../../hooks/useOperatorOverviewQuery'
import { useOperatorAggregatesQuery } from '../../../hooks/useOperatorAggregatesQuery'
import OverviewCards from './components/OverviewCards'
import AggregatesChart from './components/AggregatesChart'
import ContainerHistoryPanel from './components/ContainerHistoryPanel'
import './styles/operator-dashboard.css'

export default function OperatorDashboardPage() {
  const [granularity, setGranularity] = useState('1h')
  const [metric, setMetric] = useState('fill_level')
  const [groupBy, setGroupBy] = useState('waste_type')

  const { data: overviewData, isLoading: overviewLoading, error: overviewError } = useOperatorOverviewQuery()

  const { data: aggregatesData, isLoading: aggregatesLoading, error: aggregatesError } = useOperatorAggregatesQuery({
    granularity,
    metric,
  })

  return (
    <div className="operator-dashboard-page">
      <header className="operator-dashboard-page__header">
        <h1>Dashboard</h1>
        <p className="text-secondary">System overview and analytics</p>
      </header>

      {overviewError && <div className="error-state">Error loading overview: {overviewError.message}</div>}
      {!overviewError && <OverviewCards data={overviewData} isLoading={overviewLoading} />}

      <div className="operator-dashboard-page__section">
        <h2>Container Analytics</h2>
        <div className="dashboard-controls">
          <div className="control-group">
            <label>Granularity</label>
            <select value={granularity} onChange={(e) => setGranularity(e.target.value)} className="select">
              <option value="1h">Hourly</option>
              <option value="1d">Daily</option>
              <option value="1w">Weekly</option>
            </select>
          </div>

          <div className="control-group">
            <label>Metric</label>
            <select value={metric} onChange={(e) => setMetric(e.target.value)} className="select">
              <option value="fill_level">Fill Level</option>
              <option value="battery_level">Battery Level</option>
              <option value="temperature">Temperature</option>
            </select>
          </div>

          <div className="control-group">
            <label>Group By</label>
            <select value={groupBy} onChange={(e) => setGroupBy(e.target.value)} className="select">
              <option value="waste_type">Waste Type</option>
              <option value="location">Location</option>
            </select>
          </div>
        </div>

        {aggregatesError && <div className="error-state">Error loading aggregates: {aggregatesError.message}</div>}
        {!aggregatesError && (
          <AggregatesChart data={aggregatesData} isLoading={aggregatesLoading} metric={metric} />
        )}
      </div>

      <div className="operator-dashboard-page__section">
        <h2>Container History</h2>
        <ContainerHistoryPanel />
      </div>
    </div>
  )
}
