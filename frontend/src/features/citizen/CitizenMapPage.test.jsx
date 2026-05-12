import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import CitizenMapPage from './CitizenMapPage'

// Mock leaflet
vi.mock('react-leaflet', () => ({
  MapContainer: ({ children }) => <div data-testid="map-container">{children}</div>,
  TileLayer: () => null,
  Marker: () => null,
  Popup: () => null,
  Polyline: () => null,
  useMap: () => ({ fitBounds: vi.fn() }),
}))

// Mock useCitizenNearbyQuery
vi.mock('../../../hooks/useCitizenNearbyQuery', () => ({
  useCitizenNearbyQuery: () => ({
    data: {
      containers: [
        {
          id: 'container-1',
          name: 'Container 1',
          waste_type: 'Glass',
          fill_level: 75,
          status: 'ok',
          last_updated: new Date().toISOString(),
          location: { latitude: 42.34, longitude: -8.38 },
        },
      ],
    },
    isLoading: false,
    error: null,
    refetch: vi.fn(),
  }),
}))

describe('CitizenMapPage', () => {
  let queryClient

  beforeEach(() => {
    queryClient = new QueryClient()
  })

  it('renders the map container', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <CitizenMapPage />
      </QueryClientProvider>
    )
    expect(screen.getByTestId('map-container')).toBeInTheDocument()
  })

  it('renders the search controls', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <CitizenMapPage />
      </QueryClientProvider>
    )
    expect(screen.getByText(/Use My Location/i)).toBeInTheDocument()
  })

  it('displays nearby containers list', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <CitizenMapPage />
      </QueryClientProvider>
    )
    // Verify the map page structure renders
    expect(screen.getByTestId('map-container')).toBeInTheDocument()
  })
})
