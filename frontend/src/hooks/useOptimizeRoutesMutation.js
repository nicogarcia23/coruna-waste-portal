import { useMutation } from '@tanstack/react-query'
import { optimizeRoutes } from '../services/api'

export function useOptimizeRoutesMutation() {
  return useMutation({
    mutationFn: optimizeRoutes,
  })
}
