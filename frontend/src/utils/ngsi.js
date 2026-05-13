export function getProp(entity, attr) {
  if (!entity) return null
  const field = entity[attr]
  if (field === null || field === undefined) return null
  if (typeof field === 'object' && 'value' in field) {
    return field.value
  }
  return field
}

export default getProp
