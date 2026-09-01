import { useState, useEffect } from 'react'
import './AlertsPanel.css'

function AlertsPanel() {
  const [alerts, setAlerts] = useState([])
  const [newAlert, setNewAlert] = useState({
    severity: 'medium',
    message: '',
    language: 'en'
  })

  useEffect(() => {
    fetchAlerts()
  }, [])

  const fetchAlerts = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/alerts/`)
      const data = await response.json()
      setAlerts(data)
    } catch (error) {
      console.error('Error fetching alerts:', error)
    }
  }

  const handleBroadcast = async (e) => {
    e.preventDefault()
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/alerts/broadcast`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newAlert)
      })

      if (response.ok) {
        setNewAlert({ severity: 'medium', message: '', language: 'en' })
        fetchAlerts()
      }
    } catch (error) {
      console.error('Error broadcasting alert:', error)
      alert('Error broadcasting alert')
    }
  }

  const getSeverityIcon = (severity) => {
    switch(severity) {
      case 'high': return '🔴'
      case 'medium': return '🟡'
      case 'low': return '🟢'
      default: return '⚪'
    }
  }

  const getSeverityClass = (severity) => {
    switch(severity) {
      case 'high': return 'high'
      case 'medium': return 'medium'
      case 'low': return 'low'
      default: return ''
    }
  }

  return (
    <div className="alerts-panel">
      <div className="alerts-header">
        <h2>🔔 Alerts & Notifications</h2>
        <p>Multilingual alerts for districts, transporters, and field teams</p>
        <span className="multilingual-badge">English + Hindi Support</span>
      </div>

      <div className="alerts-content">
        <div className="broadcast-form">
          <h3>Broadcast New Alert</h3>
          <form onSubmit={handleBroadcast}>
            <div className="form-group">
              <label htmlFor="severity">Severity</label>
              <select
                id="severity"
                value={newAlert.severity}
                onChange={(e) => setNewAlert({...newAlert, severity: e.target.value})}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="language">Language</label>
              <select
                id="language"
                value={newAlert.language}
                onChange={(e) => setNewAlert({...newAlert, language: e.target.value})}
              >
                <option value="en">English</option>
                <option value="hi">Hindi</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="message">Alert Message</label>
              <textarea
                id="message"
                value={newAlert.message}
                onChange={(e) => setNewAlert({...newAlert, message: e.target.value})}
                rows="3"
                placeholder="Enter alert message..."
                required
              />
            </div>

            <button type="submit" className="btn-primary">
              📢 Broadcast Alert
            </button>
          </form>
        </div>

        <div className="active-alerts">
          <h3>Active Alerts</h3>
          {alerts.length === 0 ? (
            <p className="no-alerts">No active alerts</p>
          ) : (
            <div className="alerts-list">
              {alerts.map(alert => (
                <div key={alert.id} className={`alert-item ${getSeverityClass(alert.severity)}`}>
                  <div className="alert-header">
                    <span className="severity-icon">{getSeverityIcon(alert.severity)}</span>
                    <span className="severity-text">{alert.severity.toUpperCase()}</span>
                    <span className="alert-language">{alert.language.toUpperCase()}</span>
                  </div>
                  <p className="alert-message">{alert.message}</p>
                  <div className="alert-footer">
                    <span className="alert-time">
                      {new Date(alert.created_at).toLocaleString()}
                    </span>
                    <span className="alert-status">Active</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="alerts-info">
        <h3>Alert Categories</h3>
        <div className="alert-types">
          <div className="type-card high">
            <span className="type-icon">🔴</span>
            <h4>High Priority</h4>
            <p>Critical road closures, emergency situations</p>
          </div>
          <div className="type-card medium">
            <span className="type-icon">🟡</span>
            <h4>Medium Priority</h4>
            <p>Risk warnings, weather advisories</p>
          </div>
          <div className="type-card low">
            <span className="type-icon">🟢</span>
            <h4>Low Priority</h4>
            <p>General updates, informational alerts</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AlertsPanel
