import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import RoutePlannerPage from './RoutePlannerPage'

// Mock leaflet
vi.mock('react-leaflet', () => ({
  MapContainer: ({ children }) => <div data-testid="map-container">{children}</div>,
  TileLayer: () => null,
  Marker: () => null,
  Popup: () => null,
  Polyline: () => null,
  CircleMarker: () => null,
}))

// Mock leaflet
vi.mock('leaflet', () => ({
  default: {
    divIcon: ({ html }) => ({ html }),
  },
}))

// Mock mutation hook
vi.mock('../../../hooks/useOptimizeRoutesMutation', () => ({
  useOptimizeRoutesMutation: () => ({
    mutate: vi.fn(),
    isPending: false,
  }),
}))

describe('RoutePlannerPage', () => {
  let queryClient

  beforeEach(() => {
    queryClient = new QueryClient()
  })

  it('renders route planner form', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <RoutePlannerPage />
        </BrowserRouter>
      </QueryClientProvider>
    )
    expect(screen.getByText('Route Configuration')).toBeInTheDocument()
  })

  it('renders empty state when no results', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <RoutePlannerPage />
        </BrowserRouter>
      </QueryClientProvider>
    )
    expect(screen.getByText(/Fill out the form and click/i)).toBeInTheDocument()
  })

  it('has waste type checkboxes', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <RoutePlannerPage />
        </BrowserRouter>
      </QueryClientProvider>
    )
    expect(screen.getByLabelText('Glass')).toBeInTheDocument()
    expect(screen.getByLabelText('Plastic')).toBeInTheDocument()
  })

  it('has optimize routes button', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <RoutePlannerPage />
        </BrowserRouter>
      </QueryClientProvider>
    )
    expect(screen.getByText('Optimize Routes')).toBeInTheDocument()
  })
})
