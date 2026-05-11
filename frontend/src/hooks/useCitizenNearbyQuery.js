import { useQuery } from '@tanstack/react-query'
import { getNearbyContainers } from '../services/api'

export function useCitizenNearbyQuery(params) {
  const { lat = null, lon = null, radius = 500, wasteType = [], limit = 50 } = params || {}

  return useQuery({
    queryKey: ['nearby', lat, lon, radius, wasteType],
    queryFn: () => getNearbyContainers(lat, lon, radius, wasteType, limit),
    enabled: lat !== null && lon !== null,
    staleTime: 15_000,
    refetchInterval: 30_000,
  })
}
