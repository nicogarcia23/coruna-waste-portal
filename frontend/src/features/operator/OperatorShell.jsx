import { Navigate, Outlet } from 'react-router-dom'
import { isAuthenticated } from '../../services/auth'

export default function OperatorShell() {
  if (!isAuthenticated()) {
    return <Navigate to="/operator/login" replace />
  }

  return (
    <div className="operator-shell">
      <Outlet />
    </div>
  )
}
