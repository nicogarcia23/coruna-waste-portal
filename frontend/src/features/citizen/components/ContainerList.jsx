import { formatFillLevel, formatDistance, formatTimestamp, getStatusLabel } from '../../../utils/format'
import '../styles/container-list.css'

function getFillLevelCategory(fillLevel) {
  if (fillLevel === null || fillLevel === undefined || Number.isNaN(fillLevel)) return null
  const level = Number(fillLevel)
  if (level < 50) return 'low'
  if (level < 75) return 'medium'
  return 'high'
}

function FillLevelBar({ fillLevel }) {
  if (fillLevel === null || fillLevel === undefined || Number.isNaN(fillLevel)) {
    return <div className="container-list__item-body">Sin datos</div>
  }

  const category = getFillLevelCategory(fillLevel)
  const percentage = Math.min(Math.max(Number(fillLevel), 0), 100)

  return (
    <div className="fill-level-container">
      <span className="label">Llenado:</span>
      <div className="fill-level-bar">
        <div
          className={`fill-level-bar__progress fill-level-bar__progress--${category}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="fill-level-text">{formatFillLevel(fillLevel)}</span>
    </div>
  )
}

export default function ContainerList({ containers, selectedId, onSelect }) {
  return (
    <div className="container-list">
      <div className="container-list__header">
        <h4>Nearby Containers ({containers.length})</h4>
      </div>
      <ul className="container-list__items">
        {containers.map((container) => (
          <li
            key={container.id}
            className={`container-list__item ${selectedId === container.id ? 'container-list__item--active' : ''}`}
            onClick={() => onSelect(container.id)}
          >
            <div className="container-list__item-header">
              <strong>{container.name}</strong>
              <span className={`waste-type-badge waste-type-badge--${container.waste_type.toLowerCase()}`}>
                {container.waste_type}
              </span>
            </div>
            <div className="container-list__item-body">
              <FillLevelBar fillLevel={container.fill_level} />
              
              <div>
                <span className="label">Status:</span>{' '}
                <span
                  className={`status-badge status-badge--${container.status.toLowerCase().replace(/_/g, '-')}`}
                >
                  {getStatusLabel(container.status)}
                </span>
              </div>

              {container.distance !== undefined && (
                <div className="distance-info">
                  <span className="label">Distance:</span>{' '}
                  <span className="distance-value">{formatDistance(container.distance)}</span>
                </div>
              )}

              <div className="timestamp-info">
                <span className="label">Last seen:</span> {formatTimestamp(container.last_updated)}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
