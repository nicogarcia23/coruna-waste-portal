import { useCallback, useEffect, useMemo, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet'
import { useCitizenNearbyQuery } from '../../hooks/useCitizenNearbyQuery'
import NearbySearchControls from './components/NearbySearchControls'
import ContainerList from './components/ContainerList'
import { createContainerIcon } from '../../utils/map'
import './styles/citizen-map.css'

export default function CitizenMapPage() {
  const [lat, setLat] = useState(null)
  const [lon, setLon] = useState(null)
  const [radius, setRadius] = useState(500)
  const [wasteTypes, setWasteTypes] = useState(['Glass', 'Plastic', 'Metal', 'Organic', 'Paper'])
  const [selectedContainer, setSelectedContainer] = useState(null)
  const [mapCenter, setMapCenter] = useState([42.3401, -8.3885]) // Default A Coruña center

  const { data, isLoading, error, refetch } = useCitizenNearbyQuery(
    lat && lon ? { lat, lon, radius, waste_types: wasteTypes } : null
  )

  const containers = data?.containers || []

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

  const markers = useMemo(
    () =>
      containers.map((container) => ({
        id: container.id,
        position: [container.location.latitude, container.location.longitude],
        container,
      })),
    [containers]
  )

  const userLocation = lat && lon ? [lat, lon] : null

  return (
    <div className="citizen-map-page">
      <aside className="citizen-map-page__sidebar">
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
        <MapContainer center={mapCenter} zoom={13} className="map-container">
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
                positions={userLocation}
                color="blue"
                weight={2}
                radius={radius}
                dashArray="5, 5"
                interactive={false}
              />
            </>
          )}

          {markers.map(({ id, position, container }) => (
            <Marker
              key={id}
              position={position}
              icon={createContainerIcon(container.waste_type, container.fill_level)}
              eventHandlers={{
                click: () => setSelectedContainer(id),
              }}
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
          ))}
        </MapContainer>
      </div>
    </div>
  )
}
