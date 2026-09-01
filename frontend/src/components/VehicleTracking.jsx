import { useState, useEffect } from 'react'
import './VehicleTracking.css'

function VehicleTracking() {
  const [vehicles, setVehicles] = useState([])
  const [selectedVehicle, setSelectedVehicle] = useState(null)

  useEffect(() => {
    fetchVehicles()
  }, [])

  const fetchVehicles = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/vehicles/')
      const data = await response.json()
      setVehicles(data)
    } catch (error) {
      console.error('Error fetching vehicles:', error)
    }
  }

  const trackVehicle = async (vehicleId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/vehicles/${vehicleId}/track`)
      const data = await response.json()
      setSelectedVehicle(data)
    } catch (error) {
      console.error('Error tracking vehicle:', error)
    }
  }

  const getCargoIcon = (cargoType) => {
    switch(cargoType) {
      case 'medicine': return '💊'
      case 'food': return '🍚'
      case 'agricultural': return '🌾'
      case 'construction': return '🏗️'
      default: return '📦'
    }
  }

  const getStatusColor = (status) => {
    switch(status) {
      case 'active': return '#22c55e'
      case 'delayed': return '#f59e0b'
      case 'arrived': return '#3b82f6'
      default: return '#6b7280'
    }
  }

  return (
    <div className="vehicle-tracking">
      <div className="tracking-header">
        <h2>🚚 Essential Goods Vehicle Tracking</h2>
        <p>Real-time tracking of vehicles carrying essential supplies across NER</p>
        <span className="simulation-badge">SIMULATION - Demo Data</span>
      </div>

      <div className="tracking-content">
        <div className="vehicles-list">
          <h3>Active Vehicles</h3>
          {vehicles.map(vehicle => (
            <div 
              key={vehicle.id}
              className={`vehicle-card ${selectedVehicle?.vehicle_id === vehicle.vehicle_id ? 'selected' : ''}`}
              onClick={() => trackVehicle(vehicle.vehicle_id)}
            >
              <div className="vehicle-header">
                <span className="vehicle-id">{vehicle.vehicle_id}</span>
                <span className="vehicle-cargo">{getCargoIcon(vehicle.cargo_type)} {vehicle.cargo_type}</span>
              </div>
              <div className="vehicle-status">
                <span 
                  className="status-indicator"
                  style={{ backgroundColor: getStatusColor(vehicle.status) }}
                ></span>
                <span className="status-text">{vehicle.status.toUpperCase()}</span>
              </div>
              <div className="vehicle-details">
                <p>ETA: {vehicle.eta_minutes} minutes</p>
                <p>Route Risk: {vehicle.route_risk_score.toFixed(1)}/100</p>
              </div>
            </div>
          ))}
        </div>

        {selectedVehicle && (
          <div className="vehicle-details-panel">
            <h3>Vehicle Details: {selectedVehicle.vehicle_id}</h3>
            <div className="detail-grid">
              <div className="detail-item">
                <label>Cargo Type</label>
                <span>{getCargoIcon(selectedVehicle.cargo_type)} {selectedVehicle.cargo_type}</span>
              </div>
              <div className="detail-item">
                <label>Status</label>
                <span style={{ color: getStatusColor(selectedVehicle.status) }}>
                  {selectedVehicle.status.toUpperCase()}
                </span>
              </div>
              <div className="detail-item">
                <label>Current Position</label>
                <span>
                  {selectedVehicle.current_position.lat.toFixed(4)}, {selectedVehicle.current_position.lon.toFixed(4)}
                </span>
              </div>
              <div className="detail-item">
                <label>Destination</label>
                <span>
                  {selectedVehicle.destination.lat.toFixed(4)}, {selectedVehicle.destination.lon.toFixed(4)}
                </span>
              </div>
              <div className="detail-item">
                <label>ETA</label>
                <span>{selectedVehicle.eta_minutes} minutes</span>
              </div>
              <div className="detail-item">
                <label>Route Risk Score</label>
                <span className={selectedVehicle.route_risk_score > 50 ? 'high-risk' : 'normal-risk'}>
                  {selectedVehicle.route_risk_score.toFixed(1)}/100
                </span>
              </div>
              <div className="detail-item">
                <label>Last Updated</label>
                <span>{new Date(selectedVehicle.last_updated).toLocaleString()}</span>
              </div>
            </div>
            <button className="btn-refresh" onClick={() => trackVehicle(selectedVehicle.vehicle_id)}>
              🔄 Refresh Position
            </button>
          </div>
        )}
      </div>

      <div className="tracking-info">
        <h3>Vehicle Categories</h3>
        <div className="vehicle-types">
          <div className="type-card">
            <span className="type-icon">💊</span>
            <h4>Medicine</h4>
            <p>Medical supplies and emergency drugs</p>
          </div>
          <div className="type-card">
            <span className="type-icon">🍚</span>
            <h4>Food</h4>
            <p>Essential food supplies and rations</p>
          </div>
          <div className="type-card">
            <span className="type-icon">🌾</span>
            <h4>Agricultural</h4>
            <p>Farm produce and agricultural inputs</p>
          </div>
          <div className="type-card">
            <span className="type-icon">🏗️</span>
            <h4>Construction</h4>
            <p>Building materials and equipment</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default VehicleTracking
