import { useState } from 'react'
import RouteRequestForm from './components/RouteRequestForm'
import RouteResultsMap from './components/RouteResultsMap'
import RouteSummaryPanel from './components/RouteSummaryPanel'
import { useOptimizeRoutesMutation } from '../../../hooks/useOptimizeRoutesMutation'
import './components/styles/route-planner.css'

export default function RoutePlannerPage() {
  const [results, setResults] = useState(null)
  const { mutate, isPending } = useOptimizeRoutesMutation({
    onSuccess: (data) => setResults(data),
  })

  const handleOptimize = (formData) => {
    mutate(formData)
  }

  return (
    <div className="route-planner-page">
      <aside className="route-planner-page__sidebar">
        <RouteRequestForm onSubmit={handleOptimize} isLoading={isPending} />

        {results && (
          <div className="route-planner-page__summary">
            <RouteSummaryPanel results={results} />
          </div>
        )}
      </aside>

      <div className="route-planner-page__map">
        {results ? (
          <RouteResultsMap results={results} />
        ) : (
          <div className="route-planner-page__empty">
            <div className="empty-state">
              <h3>Route Planner</h3>
              <p>Fill out the form and click "Optimize Routes" to see results on the map.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
