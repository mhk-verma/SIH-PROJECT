import { useState } from 'react'
import './IncidentReport.css'

function IncidentReport() {
  const [formData, setFormData] = useState({
    incident_type: 'landslide',
    description: '',
    latitude: '',
    longitude: '',
    severity: 'medium',
    photo_url: ''
  })

  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/incidents/report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        setSubmitted(true)
        setFormData({
          incident_type: 'landslide',
          description: '',
          latitude: '',
          longitude: '',
          severity: 'medium',
          photo_url: ''
        })
      }
    } catch (error) {
      console.error('Error submitting incident:', error)
      alert('Error submitting incident. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const getLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData({
            ...formData,
            latitude: position.coords.latitude.toFixed(6),
            longitude: position.coords.longitude.toFixed(6)
          })
        },
        (error) => {
          console.error('Error getting location:', error)
          alert('Unable to get your location. Please enter manually.')
        }
      )
    } else {
      alert('Geolocation is not supported by your browser.')
    }
  }

  if (submitted) {
    return (
      <div className="incident-report success">
        <div className="success-message">
          <h2>✓ Incident Reported Successfully</h2>
          <p>Your incident has been submitted and will be reviewed by field officers.</p>
          <button onClick={() => setSubmitted(false)} className="btn-secondary">
            Report Another Incident
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="incident-report">
      <div className="report-header">
        <h2>🚨 Report Incident</h2>
        <p>Submit field reports for road disruptions, landslides, floods, etc.</p>
        <span className="offline-badge">Offline-First: Reports sync when connection available</span>
      </div>

      <form onSubmit={handleSubmit} className="incident-form">
        <div className="form-group">
          <label htmlFor="incident_type">Incident Type *</label>
          <select
            id="incident_type"
            name="incident_type"
            value={formData.incident_type}
            onChange={handleChange}
            required
          >
            <option value="landslide">Landslide</option>
            <option value="flood">Flood</option>
            <option value="bridge_damage">Bridge Damage</option>
            <option value="road_blockage">Road Blockage</option>
            <option value="traffic">Traffic</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="description">Description *</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            rows="4"
            placeholder="Describe the incident in detail..."
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="latitude">Latitude *</label>
            <div className="location-input">
              <input
                type="text"
                id="latitude"
                name="latitude"
                value={formData.latitude}
                onChange={handleChange}
                required
                placeholder="25.123456"
                step="0.000001"
              />
              <button type="button" onClick={getLocation} className="btn-location">
                📍 Get Location
              </button>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="longitude">Longitude *</label>
            <input
              type="text"
              id="longitude"
              name="longitude"
              value={formData.longitude}
              onChange={handleChange}
              required
              placeholder="91.123456"
              step="0.000001"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="severity">Severity *</label>
          <select
            id="severity"
            name="severity"
            value={formData.severity}
            onChange={handleChange}
            required
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="photo_url">Photo URL (Optional)</label>
          <input
            type="url"
            id="photo_url"
            name="photo_url"
            value={formData.photo_url}
            onChange={handleChange}
            placeholder="https://example.com/photo.jpg"
          />
        </div>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Submitting...' : 'Submit Incident Report'}
        </button>
      </form>

      <div className="report-info">
        <h3>Recent Incidents</h3>
        <div className="recent-incidents">
          <div className="incident-item">
            <span className="incident-type">LANDSLIDE</span>
            <span className="incident-location">NH-44 near Shillong</span>
            <span className="incident-status verified">✓ Verified</span>
          </div>
          <div className="incident-item">
            <span className="incident-type">FLOOD</span>
            <span className="incident-location">NH-37 Kamrup</span>
            <span className="incident-status verified">✓ Verified</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default IncidentReport
