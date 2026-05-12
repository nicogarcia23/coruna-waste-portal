import { MapContainer, TileLayer, Marker, Popup, Polyline, CircleMarker } from 'react-leaflet'
import L from 'leaflet'
import './styles/route-results-map.css'

const VEHICLE_COLORS = [
  '#FF6B6B',
  '#4ECDC4',
  '#45B7D1',
  '#FFA07A',
  '#98D8C8',
  '#F7DC6F',
  '#BB8FCE',
  '#85C1E2',
]

function createStopMarker(color) {
  return L.divIcon({
    html: `<div style="background: ${color}; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">📍</div>`,
    className: 'stop-marker',
    iconSize: [28, 28],
  })
}

function createDepotMarker() {
  return L.divIcon({
    html: '<div style="font-size: 24px;">⭐</div>',
    className: 'depot-marker',
    iconSize: [24, 24],
  })
}

function createUnassignedMarker() {
  return L.divIcon({
    html: '<div style="font-size: 24px;">❌</div>',
    className: 'unassigned-marker',
    iconSize: [24, 24],
  })
}

export default function RouteResultsMap({ results }) {
  const { routes, unassigned, depot } = results

  function extractLatLonFrom(obj) {
    try {
      const coords = obj?.location?.value?.coordinates
      if (coords && Array.isArray(coords) && coords.length >= 2) {
        const lon = Number(coords[0])
        const lat = Number(coords[1])
        if (!Number.isFinite(lat) || !Number.isFinite(lon)) return null
        return [lat, lon]
      }
      if (obj?.location?.latitude != null && obj?.location?.longitude != null) {
        const lat = Number(obj.location.latitude)
        const lon = Number(obj.location.longitude)
        if (!Number.isFinite(lat) || !Number.isFinite(lon)) return null
        return [lat, lon]
      }
      return null
    } catch (e) {
      return null
    }
  }

  const depotLocation = extractLatLonFrom(depot) || [0, 0]
  let mapCenter = depotLocation

  if (routes.length > 0 && routes[0].stops.length > 0) {
    const stops = routes[0].stops
    const first = extractLatLonFrom(stops[0])
    if (first) mapCenter = first
  }

  return (
    <div className="route-results-map">
      <MapContainer center={mapCenter} zoom={13} className="map-container">
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {/* Depot */}
        {depotLocation && (
          <Marker position={depotLocation} icon={createDepotMarker()}>
          <Popup>
            <strong>Depot</strong>
            <br />
            {depotLocation[0].toFixed(4)}, {depotLocation[1].toFixed(4)}
          </Popup>
          </Marker>
        )}

        {/* Routes */}
          {routes.map((route, routeIdx) => {
          const color = VEHICLE_COLORS[routeIdx % VEHICLE_COLORS.length]
            const polylinePositions = route.geometry
              ? route.geometry
                  .filter((coord) => coord && Array.isArray(coord) && coord.length >= 2)
                  .map((coord) => [coord[1], coord[0]])
              : route.stops
                  .map((stop) => extractLatLonFrom(stop))
                  .filter(Boolean)

          return (
            <div key={`route-${routeIdx}`}>
              {/* Polyline */}
              {polylinePositions && polylinePositions.length > 0 && (
                <Polyline
                  positions={polylinePositions}
                  color={color}
                  weight={3}
                  opacity={0.8}
                  dashArray={route.geometry_type === 'osrm' ? undefined : '5, 5'}
                />
              )}

              {/* Stop markers */}
              {route.stops.map((stop, stopIdx) => {
                const pos = extractLatLonFrom(stop)
                if (!pos) return null
                return (
                  <Marker
                    key={`stop-${routeIdx}-${stopIdx}`}
                    position={pos}
                    icon={createStopMarker(color)}
                  >
                    <Popup>
                      <strong>Stop {stopIdx + 1}</strong>
                      <br />
                      ID: {stop.container_id}
                      <br />
                      Demand: {stop.demand}kg
                    </Popup>
                  </Marker>
                )
              })}
            </div>
          )
        })}

        {/* Unassigned */}
        {unassigned && unassigned.length > 0 && (
          <div>
            {unassigned.map((container) => (
              <Marker
                key={`unassigned-${container.id}`}
                position={[container.location.latitude, container.location.longitude]}
                icon={createUnassignedMarker()}
              >
                <Popup>
                  <strong>Unassigned</strong>
                  <br />
                  ID: {container.id}
                  <br />
                  <span style={{ color: 'red' }}>No vehicle available</span>
                </Popup>
              </Marker>
            ))}
          </div>
        )}
      </MapContainer>
    </div>
  )
}
