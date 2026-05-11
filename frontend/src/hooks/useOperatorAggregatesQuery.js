import { useQuery } from '@tanstack/react-query'
import { getOperatorAggregates } from '../services/api'

export function useOperatorAggregatesQuery({ start, end, groupBy, metric, granularity }) {
  const staleTime = granularity === '1d' ? 5 * 60_000 : 2 * 60_000

  return useQuery({
    queryKey: ['aggregates', groupBy, metric, granularity, start, end],
    queryFn: () => getOperatorAggregates(start, end, groupBy, metric, granularity),
    staleTime,
  })
}
