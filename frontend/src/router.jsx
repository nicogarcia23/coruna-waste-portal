import { createBrowserRouter, Navigate } from 'react-router-dom'
import App from './App'
import CitizenMapPage from './features/citizen/CitizenMapPage'
import OperatorTokenForm from './features/operator/components/OperatorTokenForm'
import OperatorShell from './features/operator/OperatorShell'
import OperatorDashboardPage from './features/operator/dashboard/OperatorDashboardPage'
import RoutePlannerPage from './features/operator/routes/RoutePlannerPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        index: true,
        element: <CitizenMapPage />,
      },
      {
        path: 'operator/login',
        element: <OperatorTokenForm standalone />,
      },
      {
        path: 'operator',
        element: <OperatorShell />,
        children: [
          { index: true, element: <Navigate to="/operator/dashboard" replace /> },
          { path: 'dashboard', element: <OperatorDashboardPage /> },
          { path: 'routes', element: <RoutePlannerPage /> },
        ],
      },
    ],
  },
])
