import { formatFillLevel } from '../../../../utils/format'
import '../styles/overview-cards.css'

const KPI_CARDS = [
  { key: 'total_containers', label: 'Total Containers', icon: '📦' },
  { key: 'needs_collection', label: 'Needs Collection', icon: '⚠️' },
  { key: 'avg_fill_level', label: 'Avg Fill Level', icon: '📊', format: formatFillLevel },
  { key: 'out_of_service', label: 'Out of Service', icon: '⛔' },
]

export default function OverviewCards({ data, isLoading }) {
  return (
    <div className="overview-cards">
      {KPI_CARDS.map(({ key, label, icon, format }) => (
        <div key={key} className="overview-card">
          <div className="overview-card__icon">{icon}</div>
          <div className="overview-card__content">
            <div className="overview-card__label">{label}</div>
            <div className="overview-card__value">
              {isLoading ? '-' : format ? format(data?.[key] || 0) : data?.[key] || 0}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
