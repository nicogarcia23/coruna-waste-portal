export default function LoadingState({ message = 'Loading data...' }) {
  return (
    <div className="loading-state" role="status" aria-live="polite">
      <div className="spinner" />
      <span>{message}</span>
    </div>
  )
}
