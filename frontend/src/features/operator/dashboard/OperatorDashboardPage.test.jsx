import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import OperatorDashboardPage from './OperatorDashboardPage'

// Mock components
vi.mock('./components/OverviewCards', () => ({
  default: ({ data }) => (
    <div data-testid="overview-cards">
      {data?.total_containers || 0} containers
    </div>
  ),
}))

vi.mock('./components/AggregatesChart', () => ({
  default: () => <div data-testid="aggregates-chart">Chart</div>,
}))

vi.mock('./components/ContainerHistoryPanel', () => ({
  default: () => <div data-testid="container-history">History Panel</div>,
}))

// Mock hooks
vi.mock('../../../hooks/useOperatorOverviewQuery', () => ({
  useOperatorOverviewQuery: () => ({
    data: {
      total_containers: 150,
      needs_collection: 23,
      avg_fill_level: 65,
      out_of_service: 2,
    },
    isLoading: false,
    error: null,
  }),
}))

vi.mock('../../../hooks/useOperatorAggregatesQuery', () => ({
  useOperatorAggregatesQuery: () => ({
    data: { aggregates: [] },
    isLoading: false,
    error: null,
  }),
}))

describe('OperatorDashboardPage', () => {
  let queryClient

  beforeEach(() => {
    queryClient = new QueryClient()
  })

  it('renders dashboard header', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <OperatorDashboardPage />
        </BrowserRouter>
      </QueryClientProvider>
    )
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
  })

  it('renders overview cards with data', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <OperatorDashboardPage />
        </BrowserRouter>
      </QueryClientProvider>
    )
    await waitFor(() => {
      expect(screen.getByTestId('overview-cards')).toBeInTheDocument()
      expect(screen.getByText('150 containers')).toBeInTheDocument()
    })
  })

  it('renders analytics section with controls', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <OperatorDashboardPage />
        </BrowserRouter>
      </QueryClientProvider>
    )
    expect(screen.getByText('Container Analytics')).toBeInTheDocument()
    expect(screen.getByTestId('aggregates-chart')).toBeInTheDocument()
  })

  it('renders container history panel', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <OperatorDashboardPage />
        </BrowserRouter>
      </QueryClientProvider>
    )
    await waitFor(() => {
      expect(screen.getByTestId('container-history')).toBeInTheDocument()
    })
  })
})
