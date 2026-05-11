import { useMemo } from 'react'
import { Line } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

export default function AggregatesChart({ data, isLoading, metric }) {
  const chartData = useMemo(() => {
    if (!data?.aggregates || data.aggregates.length === 0) {
      return null
    }

    const labels = data.aggregates.map((agg) => new Date(agg.timestamp).toLocaleTimeString('es-ES'))
    const datasets = data.aggregates[0].values
      ? Object.entries(data.aggregates[0].values).map(([key, _], idx) => ({
          label: key,
          data: data.aggregates.map((agg) => agg.values[key] || 0),
          borderColor: `hsl(${(idx * 360) / Object.keys(data.aggregates[0].values).length}, 70%, 50%)`,
          backgroundColor: `hsla(${(idx * 360) / Object.keys(data.aggregates[0].values).length}, 70%, 50%, 0.1)`,
          tension: 0.3,
        }))
      : []

    return { labels, datasets }
  }, [data])

  if (isLoading) {
    return <div className="loading-state">Loading chart data...</div>
  }

  if (!chartData || chartData.datasets.length === 0) {
    return <div className="empty-state">No data available for this metric and granularity.</div>
  }

  return (
    <div className="aggregates-chart">
      <Line
        data={chartData}
        options={{
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: { position: 'top' },
            title: { display: false },
          },
          scales: {
            y: {
              beginAtZero: true,
              max: metric === 'fill_level' ? 100 : undefined,
            },
          },
        }}
      />
    </div>
  )
}
