import { NavLink, Outlet } from 'react-router-dom'
import { isAuthenticated } from './services/auth'

function linkClass({ isActive }) {
  return isActive ? 'nav-link nav-link--active' : 'nav-link'
}

export default function App() {
  const hasToken = isAuthenticated()

  return (
    <div>
      <header className="app-header">
        <div className="app-header__brand">Coruna Waste Portal</div>
        <nav className="app-header__nav" aria-label="Main navigation">
          <NavLink to="/" className={linkClass}>
            Map
          </NavLink>
          {hasToken ? (
            <>
              <NavLink to="/operator/dashboard" className={linkClass}>
                Dashboard
              </NavLink>
              <NavLink to="/operator/routes" className={linkClass}>
                Route Planner
              </NavLink>
            </>
          ) : (
            <NavLink to="/operator/login" className={linkClass}>
              Operator Login
            </NavLink>
          )}
        </nav>
      </header>
      <Outlet />
    </div>
  )
}
