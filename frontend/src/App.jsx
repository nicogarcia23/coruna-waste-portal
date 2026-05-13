import { NavLink, Outlet } from 'react-router-dom'
import { isAuthenticated } from './services/auth'
import './styles/app-header.css'

function linkClass({ isActive }) {
  return isActive ? 'nav-link nav-link--active' : 'nav-link'
}

function operatorLinkClass({ isActive }) {
  return isActive ? 'nav-link nav-link--operator-login nav-link--active' : 'nav-link nav-link--operator-login'
}

export default function App() {
  const hasToken = isAuthenticated()

  return (
    <div>
      <header className="app-header">
        <div className="app-header__brand">♻️ Portal de Gestión de Residuos — A Coruña</div>
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
            <NavLink to="/operator/login" className={operatorLinkClass}>
              Acceso Operador
            </NavLink>
          )}
        </nav>
      </header>
      <Outlet />
    </div>
  )
}
