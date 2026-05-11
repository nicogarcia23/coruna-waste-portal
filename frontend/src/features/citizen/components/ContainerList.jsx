import { formatFillLevel, formatDistance, formatTimestamp } from '../../../utils/format'
import '../styles/container-list.css'

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
              <div>
                <span className="label">Fill:</span> {formatFillLevel(container.fill_level)}
              </div>
              <div>
                <span className="label">Status:</span>{' '}
                <span
                  className={`status-badge status-badge--${container.status.toLowerCase().replace(/_/g, '-')}`}
                >
                  {container.status}
                </span>
              </div>
              {container.distance !== undefined && (
                <div>
                  <span className="label">Distance:</span> {formatDistance(container.distance)}
                </div>
              )}
              <div>
                <span className="label">Last seen:</span> {formatTimestamp(container.last_updated)}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
