export default function EmptyState({ message = 'No results found' }) {
  return (
    <div className="empty-state panel">
      <span aria-hidden>○</span>
      <p>{message}</p>
    </div>
  )
}
