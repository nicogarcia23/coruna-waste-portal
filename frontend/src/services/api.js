import { request } from './http'

export async function getNearbyContainers(lat, lon, radius = 500, wasteType = '', limit = 50) {
  return request('/api/v1/containers/nearby', {
    query: { lat, lon, radius, wasteType, limit },
  })
}

export async function getContainerStatus(id) {
  return request(`/api/v1/containers/${id}/status`)
}

export async function getOperatorOverview(isleId = '', wasteType = '') {
  return request('/api/v1/operators/containers/overview', {
    query: { isle_id: isleId, wasteType },
    auth: true,
  })
}

export async function getOperatorAggregates(
  start,
  end,
  groupBy = 'isle',
  metric = 'avg',
  granularity = '1h'
) {
  return request('/api/v1/operators/containers/aggregates', {
    query: {
      start,
      end,
      group_by: groupBy,
      metric,
      granularity,
    },
    auth: true,
  })
}

export async function getContainerHistory(id, start, end, limit = 100, offset = 0) {
  return request(`/api/v1/operators/containers/${id}/history`, {
    query: { start, end, limit, offset },
    auth: true,
  })
}

export async function optimizeRoutes(payload) {
  return request('/api/v1/operators/routes/optimize', {
    method: 'POST',
    auth: true,
    body: payload,
  })
}
