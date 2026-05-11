import L from 'leaflet'

export function getFillColor(fillLevel = 0) {
  if (fillLevel > 100) return 'var(--color-fill-overflow)'
  if (fillLevel >= 75) return 'var(--color-fill-high)'
  if (fillLevel >= 40) return 'var(--color-fill-medium)'
  return 'var(--color-fill-low)'
}

export function getWasteTypeColor(type = 'general') {
  const map = {
    organic: 'var(--color-organic)',
    paper: 'var(--color-paper)',
    glass: 'var(--color-glass)',
    plastic: 'var(--color-plastic)',
    general: 'var(--color-general)',
  }
  return map[type] || map.general
}

function getShape(type) {
  const shapes = {
    organic: 'leaf',
    paper: 'square',
    glass: 'diamond',
    plastic: 'circle',
    general: 'hexagon',
  }
  return shapes[type] || 'circle'
}

export function createContainerIcon(wasteType, fillLevel) {
  const wasteColor = getWasteTypeColor(wasteType)
  const fillColor = getFillColor(fillLevel)
  const shape = getShape(wasteType)

  return L.divIcon({
    className: 'container-icon',
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    html: `
      <div class="container-icon__outer" style="--waste-color:${wasteColor};--fill-color:${fillColor};">
        <span class="container-icon__shape container-icon__shape--${shape}"></span>
      </div>
    `,
  })
}

export function fitMapToBounds(map, markers) {
  if (!map || !markers?.length) return
  const bounds = L.latLngBounds(markers.map((m) => [m.lat, m.lon]))
  map.fitBounds(bounds, { padding: [24, 24] })
}

export function buildNumberedStopIcon(number, color) {
  return L.divIcon({
    className: 'stop-marker',
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    html: `<div class="stop-marker__bubble" style="background:${color};">${number}</div>`,
  })
}

export function buildDepotIcon() {
  return L.divIcon({
    className: 'depot-marker',
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    html: '<div class="depot-marker__star">★</div>',
  })
}

export function buildUnassignedIcon() {
  return L.divIcon({
    className: 'unassigned-marker',
    iconSize: [26, 26],
    iconAnchor: [13, 13],
    html: '<div class="unassigned-marker__x">✕</div>',
  })
}
