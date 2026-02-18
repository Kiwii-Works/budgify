import React from 'react'

const TestPage: React.FC = () => {
  return (
    <div style={{
      width: '100%',
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexDirection: 'column',
      backgroundColor: '#f0f9ff',
      fontFamily: 'system-ui, sans-serif'
    }}>
      <h1 style={{ fontSize: '48px', color: '#0ea5e9', margin: '0 0 20px 0' }}>✅ ¡Budgify Funciona!</h1>
      <p style={{ fontSize: '18px', color: '#666', margin: '0 0 30px 0' }}>React y Vite están cargando correctamente</p>
      
      <div style={{
        backgroundColor: 'white',
        padding: '30px',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        maxWidth: '500px',
        textAlign: 'center'
      }}>
        <p style={{ color: '#333', lineHeight: '1.6', margin: '0' }}>
          Si ves este mensaje, significa que:
        </p>
        <ul style={{ textAlign: 'left', color: '#333', marginTop: '15px' }}>
          <li>✓ Vite está sirviendo correctamente</li>
          <li>✓ React está montando</li>
          <li>✓ El CSS básico funciona</li>
        </ul>
      </div>

      <div style={{
        marginTop: '40px',
        padding: '20px',
        backgroundColor: '#fff',
        borderRadius: '8px',
        border: '1px solid #e5e7eb'
      }}>
        <p style={{ margin: '0', color: '#666', fontSize: '14px' }}>
          Abre la consola (F12) para ver los logs de depuración
        </p>
      </div>
    </div>
  )
}

export default TestPage
