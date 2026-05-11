import { useState, useCallback } from 'react'
import './styles/route-request-form.css'

const WASTE_TYPES = ['Glass', 'Plastic', 'Metal', 'Organic', 'Paper']

export default function RouteRequestForm({ onSubmit, isLoading }) {
  const [wasteTypes, setWasteTypes] = useState(['Glass', 'Plastic'])
  const [fillThreshold, setFillThreshold] = useState(70)
  const [vehicleCount, setVehicleCount] = useState(2)
  const [vehicleCapacity, setVehicleCapacity] = useState(500)
  const [depotLat, setDepotLat] = useState('')
  const [depotLon, setDepotLon] = useState('')
  const [useGeolocation, setUseGeolocation] = useState(false)

  const handleGeolocation = useCallback(() => {
    if (!navigator.geolocation) {
      alert('Geolocation not supported')
      return
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setDepotLat(pos.coords.latitude)
        setDepotLon(pos.coords.longitude)
        setUseGeolocation(true)
      },
      () => alert('Failed to get location')
    )
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!depotLat || !depotLon) {
      alert('Please set depot location')
      return
    }
    if (wasteTypes.length === 0) {
      alert('Select at least one waste type')
      return
    }
    onSubmit({
      waste_types: wasteTypes,
      fill_threshold: fillThreshold,
      vehicle_count: vehicleCount,
      vehicle_capacity: vehicleCapacity,
      depot: {
        latitude: parseFloat(depotLat),
        longitude: parseFloat(depotLon),
      },
    })
  }

  const handleWasteTypeToggle = (type) => {
    setWasteTypes(
      wasteTypes.includes(type) ? wasteTypes.filter((t) => t !== type) : [...wasteTypes, type]
    )
  }

  return (
    <form className="route-request-form" onSubmit={handleSubmit}>
      <h3>Route Configuration</h3>

      <div className="form-section">
        <label className="form-label">Waste Types</label>
        <div className="form-checkboxes">
          {WASTE_TYPES.map((type) => (
            <label key={type} className="checkbox-label">
              <input
                type="checkbox"
                checked={wasteTypes.includes(type)}
                onChange={() => handleWasteTypeToggle(type)}
              />
              {type}
            </label>
          ))}
        </div>
      </div>

      <div className="form-section">
        <label className="form-label">
          Fill Threshold: <span className="form-value">{fillThreshold}%</span>
        </label>
        <input
          type="range"
          min="0"
          max="100"
          step="5"
          value={fillThreshold}
          onChange={(e) => setFillThreshold(parseInt(e.target.value))}
          className="form-range"
        />
      </div>

      <div className="form-section">
        <label className="form-label">
          Vehicle Count: <span className="form-value">{vehicleCount}</span>
        </label>
        <input
          type="range"
          min="1"
          max="10"
          step="1"
          value={vehicleCount}
          onChange={(e) => setVehicleCount(parseInt(e.target.value))}
          className="form-range"
        />
      </div>

      <div className="form-section">
        <label className="form-label">
          Vehicle Capacity: <span className="form-value">{vehicleCapacity}kg</span>
        </label>
        <input
          type="range"
          min="100"
          max="1000"
          step="50"
          value={vehicleCapacity}
          onChange={(e) => setVehicleCapacity(parseInt(e.target.value))}
          className="form-range"
        />
      </div>

      <div className="form-section">
        <label className="form-label">Depot Location</label>
        <button
          type="button"
          className="btn btn-secondary btn-small"
          onClick={handleGeolocation}
          disabled={isLoading}
        >
          📍 Use My Location
        </button>
        {useGeolocation && depotLat && depotLon && (
          <div className="form-hint">Using GPS location</div>
        )}
      </div>

      <div className="form-section">
        <label className="form-label">Manual Depot Coords</label>
        <div className="form-coords">
          <input
            type="number"
            placeholder="Latitude"
            step="0.0001"
            value={depotLat}
            onChange={(e) => setDepotLat(e.target.value)}
            className="form-input form-input--small"
          />
          <input
            type="number"
            placeholder="Longitude"
            step="0.0001"
            value={depotLon}
            onChange={(e) => setDepotLon(e.target.value)}
            className="form-input form-input--small"
          />
        </div>
      </div>

      <button type="submit" className="btn btn-primary btn-large" disabled={isLoading}>
        {isLoading ? 'Optimizing...' : 'Optimize Routes'}
      </button>
    </form>
  )
}
