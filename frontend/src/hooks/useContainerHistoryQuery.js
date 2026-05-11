import { useQuery } from '@tanstack/react-query'
import { getContainerHistory } from '../services/api'

export function useContainerHistoryQuery(params) {
  const { containerId = null, start, end, limit = 100, offset = 0, enabled = false } = params || {}
  
  return useQuery({
    queryKey: ['history', containerId, start, end],
    queryFn: () => getContainerHistory(containerId, start, end, limit, offset),
    enabled: Boolean(containerId) && enabled,
    staleTime: 30_000,
  })
}
