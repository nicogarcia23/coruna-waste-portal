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

  const html = `<div style="width:32px;height:32px;border-radius:50%;border:3px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.4);background:${wasteColor};display:flex;align-items:center;justify-content:center;">
      <div style="width:14px;height:14px;border-radius:50%;background:${fillColor};border:2px solid rgba(255,255,255,0.8);"></div>
    </div>`

  return L.divIcon({
    className: '',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
    html,
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
