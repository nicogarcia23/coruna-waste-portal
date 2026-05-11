import { useState } from 'react'
import '../styles/nearby-search-controls.css'

const WASTE_TYPE_OPTIONS = ['Glass', 'Plastic', 'Metal', 'Organic', 'Paper']

export default function NearbySearchControls({
  onGeolocation,
  onManualLocation,
  radius,
  onRadiusChange,
  wasteTypes,
  onWasteTypesChange,
  isLoading,
  lat,
  lon,
}) {
  const [manualLat, setManualLat] = useState('')
  const [manualLon, setManualLon] = useState('')

  const handleManualSubmit = (e) => {
    e.preventDefault()
    const latNum = parseFloat(manualLat)
    const lonNum = parseFloat(manualLon)
    if (!isNaN(latNum) && !isNaN(lonNum)) {
      onManualLocation(latNum, lonNum)
      setManualLat('')
      setManualLon('')
    }
  }

  const handleWasteTypeToggle = (type) => {
    onWasteTypesChange(
      wasteTypes.includes(type)
        ? wasteTypes.filter((t) => t !== type)
        : [...wasteTypes, type]
    )
  }

  return (
    <div className="nearby-search-controls">
      <div className="nearby-search-controls__section">
        <h3>Location</h3>
        <button
          className="btn btn-primary"
          onClick={onGeolocation}
          disabled={isLoading}
        >
          📍 Use My Location
        </button>
        {lat && lon && (
          <div className="nearby-search-controls__coords">
            Current: {lat.toFixed(4)}, {lon.toFixed(4)}
          </div>
        )}
      </div>

      <form className="nearby-search-controls__section" onSubmit={handleManualSubmit}>
        <h3>Manual Location</h3>
        <input
          type="number"
          placeholder="Latitude"
          step="0.0001"
          value={manualLat}
          onChange={(e) => setManualLat(e.target.value)}
          className="input"
        />
        <input
          type="number"
          placeholder="Longitude"
          step="0.0001"
          value={manualLon}
          onChange={(e) => setManualLon(e.target.value)}
          className="input"
        />
        <button type="submit" className="btn btn-secondary" disabled={isLoading}>
          Set Location
        </button>
      </form>

      <div className="nearby-search-controls__section">
        <h3>Radius</h3>
        <input
          type="range"
          min="100"
          max="2000"
          step="100"
          value={radius}
          onChange={(e) => onRadiusChange(parseInt(e.target.value))}
          className="slider"
        />
        <div className="nearby-search-controls__radius-label">{radius}m</div>
      </div>

      <div className="nearby-search-controls__section">
        <h3>Waste Types</h3>
        <div className="nearby-search-controls__checkboxes">
          {WASTE_TYPE_OPTIONS.map((type) => (
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
    </div>
  )
}
