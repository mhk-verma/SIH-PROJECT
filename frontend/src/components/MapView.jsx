import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Polyline, CircleMarker } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import './MapView.css'

function MapView() {
  const [districts, setDistricts] = useState([])
  const [roadSegments, setRoadSegments] = useState([])
  const [incidents, setIncidents] = useState([])
  const [vehicles, setVehicles] = useState([])
  const [selectedDistrict, setSelectedDistrict] = useState(null)

  useEffect(() => {
    fetchMapData()
  }, [])

  const fetchMapData = async () => {
    try {
      // Fetch districts
      const districtsRes = await fetch('http://localhost:8000/api/districts/')
      const districtsData = await districtsRes.json()
      setDistricts(districtsData)

      // Fetch incidents
      const incidentsRes = await fetch('http://localhost:8000/api/incidents/')
      const incidentsData = await incidentsRes.json()
      setIncidents(incidentsData)

      // Fetch vehicles
      const vehiclesRes = await fetch('http://localhost:8000/api/vehicles/')
      const vehiclesData = await vehiclesRes.json()
      setVehicles(vehiclesData)

      // Simulated road segments (in production, this would come from API)
      setRoadSegments([
        {
          id: 1,
          name: 'NH-37 Kamrup to Guwahati',
          start_lat: 26.16, start_lon: 91.76,
          end_lat: 26.14, end_lon: 91.73,
          risk_score: 35.2,
          risk_category: 'medium'
        },
        {
          id: 2,
          name: 'NH-44 Shillong to Guwahati',
          start_lat: 25.58, start_lon: 91.89,
          end_lat: 26.14, end_lon: 91.73,
          risk_score: 72.5,
          risk_category: 'high'
        },
        {
          id: 3,
          name: 'NH-2 Imphal to Dimapur',
          start_lat: 24.83, start_lon: 93.95,
          end_lat: 25.92, end_lon: 93.73,
          risk_score: 58.3,
          risk_category: 'medium'
        }
      ])
    } catch (error) {
      console.error('Error fetching map data:', error)
    }
  }

  const getRiskColor = (riskCategory) => {
    switch(riskCategory) {
      case 'high': return '#ef4444'
      case 'medium': return '#f59e0b'
      case 'low': return '#22c55e'
      default: return '#6b7280'
    }
  }

  const centerPosition = [25.8, 92.5] // Center of NER region

  return (
    <div className="map-view">
      <div className="map-header">
        <h2>GIS Risk Map - North Eastern Region</h2>
        <div className="risk-legend">
          <span className="legend-item">
            <span className="legend-color high"></span> High Risk
          </span>
          <span className="legend-item">
            <span className="legend-color medium"></span> Medium Risk
          </span>
          <span className="legend-item">
            <span className="legend-color low"></span> Low Risk
          </span>
        </div>
      </div>

      <MapContainer center={centerPosition} zoom={7} style={{ height: '500px', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* District markers */}
        {districts.map(district => (
          <CircleMarker
            key={district.id}
            center={[district.latitude, district.longitude]}
            radius={15}
            pathOptions={{
              color: getRiskColor(district.risk_category),
              fillColor: getRiskColor(district.risk_category),
              fillOpacity: 0.6
            }}
          >
            <Popup>
              <div className="popup-content">
                <h3>{district.name}</h3>
                <p>State: {district.state}</p>
                <p>Risk Score: {district.risk_score.toFixed(1)}</p>
                <p>Risk Category: {district.risk_category.toUpperCase()}</p>
              </div>
            </Popup>
          </CircleMarker>
        ))}

        {/* Road segments */}
        {roadSegments.map(road => (
          <Polyline
            key={road.id}
            positions={[
              [road.start_lat, road.start_lon],
              [road.end_lat, road.end_lon]
            ]}
            pathOptions={{
              color: getRiskColor(road.risk_category),
              weight: 4,
              opacity: 0.8
            }}
          >
            <Popup>
              <div className="popup-content">
                <h3>{road.name}</h3>
                <p>Risk Score: {road.risk_score.toFixed(1)}</p>
                <p>Risk Category: {road.risk_category.toUpperCase()}</p>
              </div>
            </Popup>
          </Polyline>
        ))}

        {/* Incident markers */}
        {incidents.map(incident => (
          <Marker
            key={incident.id}
            position={[incident.latitude, incident.longitude]}
          >
            <Popup>
              <div className="popup-content">
                <h3>Incident: {incident.incident_type}</h3>
                <p>{incident.description}</p>
                <p>Severity: {incident.severity}</p>
                <p>Status: {incident.is_verified ? '✓ Verified' : '⏳ Pending'}</p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Vehicle markers */}
        {vehicles.map(vehicle => (
          <Marker
            key={vehicle.id}
            position={[vehicle.current_lat, vehicle.current_lon]}
          >
            <Popup>
              <div className="popup-content">
                <h3>🚚 {vehicle.vehicle_id}</h3>
                <p>Cargo: {vehicle.cargo_type}</p>
                <p>Status: {vehicle.status}</p>
                <p>ETA: {vehicle.eta_minutes} minutes</p>
                <p>Route Risk: {vehicle.route_risk_score.toFixed(1)}</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      <div className="map-info">
        <p><strong>Note:</strong> This is a prototype using simulated data for demonstration purposes.</p>
        <p>Click on markers to view detailed information about districts, roads, incidents, and vehicles.</p>
      </div>
    </div>
  )
}

export default MapView
