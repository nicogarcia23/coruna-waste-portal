import { useCallback, useEffect, useMemo, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet'
import { useCitizenNearbyQuery } from '../../hooks/useCitizenNearbyQuery'
import NearbySearchControls from './components/NearbySearchControls'
import ContainerList from './components/ContainerList'
import { createContainerIcon } from '../../utils/map'
import { getProp } from '../../utils/ngsi'
import MapErrorBoundary from '../../components/common/MapErrorBoundary'
import MapLegend from './components/MapLegend'
import './styles/citizen-map.css'

const DEFAULT_CENTER = [43.3734, -8.3879]

function inferWasteType(container) {
  const candidates = ['organic', 'paper', 'glass', 'plastic', 'general']
  const haystack = `${container?.waste_type || ''} ${container?.id || ''} ${container?.name || ''}`.toLowerCase()
  return candidates.find((candidate) => haystack.includes(candidate)) || 'general'
}

function MapAutoFit({ points }) {
  const map = useMap()

  useEffect(() => {
    if (!points || points.length === 0) return

    const bounds = points.map((point) => [point[0], point[1]])
    map.fitBounds(bounds, { padding: [48, 48], maxZoom: 16 })
  }, [map, points])

  return null
}

export default function CitizenMapPage() {
  const [lat, setLat] = useState(DEFAULT_CENTER[0])
  const [lon, setLon] = useState(DEFAULT_CENTER[1])
  const [radius, setRadius] = useState(500)
  const [wasteTypes, setWasteTypes] = useState(['Glass', 'Plastic', 'Metal', 'Organic', 'Paper'])
  const [selectedContainer, setSelectedContainer] = useState(null)
  const [mapCenter, setMapCenter] = useState(DEFAULT_CENTER)

  const { data, isLoading, error, refetch } = useCitizenNearbyQuery(
    lat && lon ? { lat, lon, radius, waste_types: wasteTypes } : null
  )

  const normalizeContainer = useCallback((container) => ({
    id: container.id,
    name: getProp(container, 'name') || container.id,
    waste_type: getProp(container, 'waste_type') || getProp(container, 'containerType') || inferWasteType(container),
    fill_level: getProp(container, 'fillLevel') ?? getProp(container, 'fill_level') ?? null,
    status: getProp(container, 'status') ?? 'unknown',
    last_updated: getProp(container, 'lastUpdated') ?? getProp(container, 'last_seen') ?? getProp(container, 'lastSeen') ?? null,
    distance: container.distance,
    location: container.location,
  }), [])

  const containers = useMemo(() => {
    const rawContainers = Array.isArray(data) ? data : data?.containers || []
    return rawContainers.map(normalizeContainer)
  }, [data, normalizeContainer])

  const handleGeolocation = useCallback(() => {
    if (!navigator.geolocation) {
      alert('Geolocation not supported')
      return
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLat(pos.coords.latitude)
        setLon(pos.coords.longitude)
        setMapCenter([pos.coords.latitude, pos.coords.longitude])
      },
      (err) => alert(`Geolocation failed: ${err.message}`)
    )
  }, [])

  const handleManualLocation = useCallback((newLat, newLon) => {
    setLat(newLat)
    setLon(newLon)
    setMapCenter([newLat, newLon])
  }, [])

  function extractLatLon(container) {
    try {
      const coords = container?.location?.value?.coordinates
      if (coords && Array.isArray(coords) && coords.length >= 2) {
        const lon = Number(coords[0])
        const lat = Number(coords[1])
        if (!Number.isFinite(lat) || !Number.isFinite(lon)) return null
        return [lat, lon]
      }

      if (
        container?.location?.latitude != null &&
        container?.location?.longitude != null
      ) {
        const lat = Number(container.location.latitude)
        const lon = Number(container.location.longitude)
        if (!Number.isFinite(lat) || !Number.isFinite(lon)) return null
        return [lat, lon]
      }

      return null
    } catch (e) {
      return null
    }
  }

  const markers = useMemo(() => containers.map((c) => ({ id: c.id, position: extractLatLon(c), container: c })), [containers])
  // Temporary debug to confirm API returns containers
  useEffect(() => {
    // eslint-disable-next-line no-console
    console.log('Citizen nearby data:', data, 'normalized:', containers.length)
  }, [data, containers.length])
  const userLocation = lat && lon ? [lat, lon] : null
  const mapPoints = useMemo(() => {
    const points = [...markers.map((marker) => marker.position).filter(Boolean)]
    if (userLocation) points.push(userLocation)
    return points
  }, [markers, userLocation])

  function MapInvalidate({ watch }) {
    const map = useMap()
    useEffect(() => {
      // give layout a moment to settle, then invalidate size
      const t = setTimeout(() => {
        try { map.invalidateSize() } catch (e) { /* ignore */ }
      }, 200)
      return () => clearTimeout(t)
    }, [map, watch])
    return null
  }

  return (
    <div className="citizen-map-page">
      <aside className="citizen-map-page__sidebar">
        <div className="citizen-map-page__controls">
          <NearbySearchControls
            onGeolocation={handleGeolocation}
            onManualLocation={handleManualLocation}
            radius={radius}
            onRadiusChange={setRadius}
            wasteTypes={wasteTypes}
            onWasteTypesChange={setWasteTypes}
            isLoading={isLoading}
            lat={lat}
            lon={lon}
          />
        </div>
        <div className="citizen-map-page__results">
          {isLoading && <div className="loading-state">Searching nearby containers...</div>}
          {error && (
            <div className="error-state">
              Error: {error.message}
              <button onClick={() => refetch()}>Retry</button>
            </div>
          )}
          {!isLoading && !error && containers.length === 0 && (
            <div className="empty-state">No containers found in this area.</div>
          )}
          {!isLoading && !error && containers.length > 0 && (
            <ContainerList
              containers={containers}
              selectedId={selectedContainer}
              onSelect={setSelectedContainer}
            />
          )}
        </div>
      </aside>

      <div className="citizen-map-page__map">
        <MapErrorBoundary>
        <MapContainer center={mapCenter} zoom={13} className="map-container">
          <MapAutoFit points={mapPoints} />
          <MapInvalidate watch={containers.length} />
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; OpenStreetMap contributors'
          />

          {userLocation && (
            <>
                <Marker position={userLocation} icon={createContainerIcon('general', 0)}>
                <Popup>Your location</Popup>
              </Marker>
              <Polyline
                positions={[mapCenter, userLocation]}
                color="blue"
                weight={2}
                dashArray="5, 5"
                interactive={false}
              />
            </>
          )}

          {markers.map(({ id, position, container }) => {
            try {
              if (!position || !Array.isArray(position) || position.length < 2) return null
              const markerWasteType = inferWasteType(container)
              return (
                <Marker
                  key={id}
                  position={position}
                  icon={createContainerIcon(markerWasteType, container.fill_level ?? 0)}
                  zIndexOffset={2000}
                  riseOnHover
                  eventHandlers={{ click: () => setSelectedContainer(id) }}
                >
                  <Popup>
                    <div>
                      <strong>{container.name}</strong>
                      <div>{container.waste_type}</div>
                      <div>Fill: {Math.round(container.fill_level)}%</div>
                      <div>Last updated: {new Date(container.last_updated).toLocaleString('es-ES')}</div>
                    </div>
                  </Popup>
                </Marker>
              )
            } catch (e) {
              return null
            }
          })}
          <MapLegend />
        </MapContainer>
        </MapErrorBoundary>
      </div>
    </div>
  )
}
