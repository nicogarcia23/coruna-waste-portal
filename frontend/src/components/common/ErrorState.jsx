export default function ErrorState({ error, onRetry }) {
  return (
    <div className="error-state panel">
      <p>{error?.message || 'Unexpected error'}</p>
      {onRetry ? (
        <button type="button" onClick={onRetry}>
          Retry
        </button>
      ) : null}
    </div>
  )
}
