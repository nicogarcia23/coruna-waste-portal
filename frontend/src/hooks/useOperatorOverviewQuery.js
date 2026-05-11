import { useQuery } from '@tanstack/react-query'
import { getOperatorOverview } from '../services/api'

export function useOperatorOverviewQuery({ isleId = '', wasteType = '' }) {
  return useQuery({
    queryKey: ['overview', isleId, wasteType],
    queryFn: () => getOperatorOverview(isleId, wasteType),
    staleTime: 30_000,
  })
}
