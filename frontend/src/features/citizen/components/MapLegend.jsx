export default function MapLegend() {
  return (
    <div className="map-legend-overlay" style={{
      position: 'absolute',
      right: 12,
      bottom: 12,
      zIndex: 1000,
      background: 'white',
      padding: 12,
      borderRadius: 8,
      boxShadow: '0 2px 8px rgba(0,0,0,0.12)',
      fontSize: 12,
      lineHeight: 1.4,
    }}>
      <div style={{ marginBottom: 8, fontWeight: 600 }}>Tipo de residuo</div>
      <div style={{ display: 'flex', gap: 8, flexDirection: 'column', marginBottom: 8 }}>
        <div><span style={{ display: 'inline-block', width: 12, height: 12, background: '#4caf50', borderRadius: '50%', marginRight: 6 }}></span>Orgánico</div>
        <div><span style={{ display: 'inline-block', width: 12, height: 12, background: '#2196f3', borderRadius: '50%', marginRight: 6 }}></span>Papel</div>
        <div><span style={{ display: 'inline-block', width: 12, height: 12, background: '#00bcd4', borderRadius: '50%', marginRight: 6 }}></span>Vidrio</div>
        <div><span style={{ display: 'inline-block', width: 12, height: 12, background: '#ff9800', borderRadius: '50%', marginRight: 6 }}></span>Plástico</div>
        <div><span style={{ display: 'inline-block', width: 12, height: 12, background: '#9e9e9e', borderRadius: '50%', marginRight: 6 }}></span>General</div>
      </div>
      <div style={{ marginBottom: 6, fontWeight: 600 }}>Nivel de llenado</div>
      <div style={{ display: 'flex', gap: 8, flexDirection: 'column' }}>
        <div><span style={{ display: 'inline-block', width: 12, height: 12, background: '#4caf50', borderRadius: '50%', marginRight: 6 }}></span>Bajo (&lt;40%)</div>
        <div><span style={{ display: 'inline-block', width: 12, height: 12, background: '#ff9800', borderRadius: '50%', marginRight: 6 }}></span>Medio (40-75%)</div>
        <div><span style={{ display: 'inline-block', width: 12, height: 12, background: '#f44336', borderRadius: '50%', marginRight: 6 }}></span>Alto (&gt;75%)</div>
        <div><span style={{ display: 'inline-block', width: 12, height: 12, background: '#9c27b0', borderRadius: '50%', marginRight: 6 }}></span>Desbordamiento (&gt;100%)</div>
      </div>
    </div>
  )
}
