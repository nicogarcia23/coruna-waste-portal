import { useState } from 'react'
import { useContainerHistoryQuery } from '../../../../hooks/useContainerHistoryQuery'
import { Line } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

export default function ContainerHistoryPanel() {
  const [containerId, setContainerId] = useState('')
  const { data, isLoading, error, refetch } = useContainerHistoryQuery(containerId ? { containerId, enabled: true } : null)

  const handleSearch = (e) => {
    e.preventDefault()
    if (containerId) {
      refetch()
    }
  }

  const chartData = data?.history
    ? {
        labels: data.history.map((h) => new Date(h.timestamp).toLocaleString('es-ES')),
        datasets: [
          {
            label: 'Fill Level (%)',
            data: data.history.map((h) => h.fill_level),
            borderColor: 'rgb(66, 153, 225)',
            backgroundColor: 'rgba(66, 153, 225, 0.1)',
            yAxisID: 'y',
            tension: 0.3,
          },
          {
            label: 'Battery (%)',
            data: data.history.map((h) => h.battery_level),
            borderColor: 'rgb(76, 175, 80)',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            yAxisID: 'y1',
            tension: 0.3,
          },
        ],
      }
    : null

  return (
    <div className="container-history-panel">
      <form className="container-history-panel__form" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Enter Container ID..."
          value={containerId}
          onChange={(e) => setContainerId(e.target.value)}
          className="form-input"
        />
        <button type="submit" className="btn btn-primary" disabled={isLoading || !containerId}>
          Search
        </button>
      </form>

      {error && <div className="error-state">Error: {error.message}</div>}

      {!error && chartData && (
        <Line
          data={chartData}
          options={{
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
              legend: { position: 'top' },
            },
            scales: {
              y: {
                type: 'linear',
                display: true,
                position: 'left',
                beginAtZero: true,
                max: 100,
              },
              y1: {
                type: 'linear',
                display: true,
                position: 'right',
                beginAtZero: true,
                max: 100,
                grid: { drawOnChartArea: false },
              },
            },
          }}
        />
      )}

      {!error && !isLoading && !chartData && <div className="empty-state">Enter a container ID to view history.</div>}
    </div>
  )
}
