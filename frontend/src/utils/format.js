export function formatDistance(meters) {
  if (meters === null || meters === undefined || Number.isNaN(meters)) return '-'
  if (meters < 1000) return `${Math.round(meters)} m`
  return `${(meters / 1000).toFixed(1)} km`
}

export function formatFillLevel(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '-'
  return `${Number(value).toFixed(1)}%`
}

export function formatTimestamp(iso, timezone = 'Europe/Madrid') {
  if (!iso) return '-'
  const date = new Date(iso)
  return new Intl.DateTimeFormat('es-ES', {
    timeZone: timezone,
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date)
}

export function formatCapacity(liters) {
  if (liters === null || liters === undefined || Number.isNaN(liters)) return '-'
  if (liters < 1000) return `${Math.round(liters)} L`
  return `${(liters / 1000).toFixed(1)} m³`
}

export function getStatusLabel(status) {
  const labels = {
    ok: 'Operativo',
    needs_collection: 'Necesita vaciado',
    maintenance: 'Mantenimiento',
    out_of_service: 'Fuera de servicio',
  }
  return labels[status] || 'Desconocido'
}
