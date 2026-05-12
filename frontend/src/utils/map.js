import L from 'leaflet'

export function getFillColor(fillLevel = 0) {
  if (fillLevel > 100) return '#9c27b0'
  if (fillLevel >= 75) return '#f44336'
  if (fillLevel >= 40) return '#ff9800'
  return '#4caf50'
}

export function getWasteTypeColor(type = 'general') {
  const map = {
    organic: '#4caf50',
    paper: '#2196f3',
    glass: '#00bcd4',
    plastic: '#ff9800',
    general: '#9e9e9e',
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

  const html = `<div style="width:44px;height:44px;border-radius:50%;border:4px solid #fff;box-shadow:0 4px 12px rgba(15,23,42,0.35);background:${wasteColor};display:flex;align-items:center;justify-content:center;transform:translateY(-2px);">
      <div style="width:18px;height:18px;border-radius:50%;background:${fillColor};border:2px solid rgba(255,255,255,0.92);"></div>
    </div>`

  return L.divIcon({
    className: '',
    iconSize: [44, 44],
    iconAnchor: [22, 42],
    popupAnchor: [0, -40],
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
