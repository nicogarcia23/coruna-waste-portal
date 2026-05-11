import { useState } from 'react'
import { formatDistance } from '../../../../utils/format'
import './styles/route-summary-panel.css'

export default function RouteSummaryPanel({ results }) {
  const { routes, unassigned, vehicle_count: totalVehicles } = results
  const [expandedRoute, setExpandedRoute] = useState(null)

  const totalDistance = routes.reduce((sum, r) => sum + (r.distance || 0), 0)
  const totalTime = routes.reduce((sum, r) => sum + (r.time || 0), 0)
  const totalAssigned = routes.reduce((sum, r) => sum + r.stops.length, 0)

  return (
    <div className="route-summary-panel">
      <h4 className="route-summary-panel__title">Optimization Results</h4>

      <div className="route-summary-panel__stats">
        <div className="stat-card">
          <div className="stat-label">Total Distance</div>
          <div className="stat-value">{formatDistance(totalDistance)}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Total Time</div>
          <div className="stat-value">
            {Math.round(totalTime / 60)}
            min
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Assigned</div>
          <div className="stat-value">{totalAssigned}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Unassigned</div>
          <div className="stat-value" style={{ color: unassigned && unassigned.length > 0 ? '#d32f2f' : '#4caf50' }}>
            {unassigned ? unassigned.length : 0}
          </div>
        </div>
      </div>

      <div className="route-summary-panel__routes">
        <h5>Vehicles ({routes.length})</h5>
        <div className="routes-list">
          {routes.map((route, idx) => (
            <div key={`route-${idx}`} className="route-item">
              <button
                className={`route-item__header ${expandedRoute === idx ? 'route-item__header--expanded' : ''}`}
                onClick={() => setExpandedRoute(expandedRoute === idx ? null : idx)}
              >
                <strong>Vehicle {idx + 1}</strong>
                <span className="route-item__meta">
                  {route.stops.length} stops • {formatDistance(route.distance)}
                </span>
              </button>

              {expandedRoute === idx && (
                <div className="route-item__stops">
                  {route.stops.map((stop, stopIdx) => (
                    <div key={`stop-${stopIdx}`} className="stop-summary">
                      <span className="stop-summary__idx">{stopIdx + 1}</span>
                      <div className="stop-summary__info">
                        <div>{stop.container_id}</div>
                        <div className="stop-summary__meta">{stop.demand}kg</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {unassigned && unassigned.length > 0 && (
        <div className="route-summary-panel__unassigned">
          <h5 style={{ color: '#d32f2f' }}>Unassigned ({unassigned.length})</h5>
          <div className="unassigned-list">
            {unassigned.map((container, idx) => (
              <div key={`unassigned-${idx}`} className="unassigned-item">
                <span className="unassigned-item__id">{container.id}</span>
                <span className="unassigned-item__meta">{container.waste_type}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
