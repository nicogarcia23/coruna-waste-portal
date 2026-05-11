import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { saveToken, clearToken } from '../../../services/auth'
import './styles/operator-token-form.css'

export default function OperatorTokenForm({ standalone = false }) {
  const [token, setToken] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!token.trim()) {
      setError('Token cannot be empty')
      return
    }
    saveToken(token)
    setToken('')
    setError('')
    if (standalone) {
      navigate('/operator/dashboard')
    }
  }

  const handleClearToken = () => {
    clearToken()
    setToken('')
    navigate('/')
  }

  return (
    <div className={`operator-token-form ${standalone ? 'operator-token-form--standalone' : ''}`}>
      <div className="operator-token-form__container">
        <div className="operator-token-form__header">
          <h2>Operator Login</h2>
          <p>Enter your Bearer token to access operator features</p>
        </div>

        <form className="operator-token-form__form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="token" className="form-label">
              Bearer Token
            </label>
            <input
              id="token"
              type="password"
              placeholder="Paste your Bearer token..."
              value={token}
              onChange={(e) => {
                setToken(e.target.value)
                setError('')
              }}
              className={`form-input ${error ? 'form-input--error' : ''}`}
            />
            {error && <div className="form-error">{error}</div>}
          </div>

          <div className="operator-token-form__actions">
            <button type="submit" className="btn btn-primary btn-large">
              Login
            </button>
            <button
              type="button"
              className="btn btn-secondary btn-large"
              onClick={handleClearToken}
            >
              Clear & Logout
            </button>
          </div>
        </form>

        {!standalone && (
          <div className="operator-token-form__info">
            <p>Your token is stored securely in the browser session.</p>
          </div>
        )}
      </div>
    </div>
  )
}
