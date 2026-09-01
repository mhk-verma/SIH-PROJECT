import { useState, useEffect } from 'react'
import MapView from './MapView'
import IncidentReport from './IncidentReport'
import VehicleTracking from './VehicleTracking'
import AlertsPanel from './AlertsPanel'
import RiskAnalysis from './RiskAnalysis'
import './Dashboard.css'

function Dashboard() {
  const [activeTab, setActiveTab] = useState('map')
  const [dashboardData, setDashboardData] = useState(null)

  useEffect(() => {
    // Fetch dashboard summary data
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/dashboard/summary`)
      const data = await response.json()
      setDashboardData(data)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    }
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>SIH26002 - Smart Logistics & Accessibility Intelligence</h1>
          <p className="subtitle">North Eastern Region (NER) Decision Support Platform</p>
          <span className="prototype-badge">PROTOTYPE - Simulated Data</span>
        </div>
      </header>

      <div className="dashboard-content">
        <nav className="sidebar">
          <button 
            className={`nav-button ${activeTab === 'map' ? 'active' : ''}`}
            onClick={() => setActiveTab('map')}
          >
            🗺️ GIS Map
          </button>
          <button 
            className={`nav-button ${activeTab === 'incidents' ? 'active' : ''}`}
            onClick={() => setActiveTab('incidents')}
          >
            🚨 Incident Report
          </button>
          <button 
            className={`nav-button ${activeTab === 'vehicles' ? 'active' : ''}`}
            onClick={() => setActiveTab('vehicles')}
          >
            🚚 Vehicle Tracking
          </button>
          <button 
            className={`nav-button ${activeTab === 'alerts' ? 'active' : ''}`}
            onClick={() => setActiveTab('alerts')}
          >
            🔔 Alerts
          </button>
          <button 
            className={`nav-button ${activeTab === 'risk' ? 'active' : ''}`}
            onClick={() => setActiveTab('risk')}
          >
            📊 Risk Analysis
          </button>
        </nav>

        <main className="main-content">
          {dashboardData && (
            <div className="summary-cards">
              <div className="summary-card">
                <h3>Districts</h3>
                <p className="card-value">{dashboardData.overview.total_districts}</p>
              </div>
              <div className="summary-card">
                <h3>Road Segments</h3>
                <p className="card-value">{dashboardData.overview.total_road_segments}</p>
              </div>
              <div className="summary-card warning">
                <h3>Active Incidents</h3>
                <p className="card-value">{dashboardData.overview.active_incidents}</p>
              </div>
              <div className="summary-card success">
                <h3>Active Vehicles</h3>
                <p className="card-value">{dashboardData.overview.active_vehicles}</p>
              </div>
            </div>
          )}

          <div className="tab-content">
            {activeTab === 'map' && <MapView />}
            {activeTab === 'incidents' && <IncidentReport />}
            {activeTab === 'vehicles' && <VehicleTracking />}
            {activeTab === 'alerts' && <AlertsPanel />}
            {activeTab === 'risk' && <RiskAnalysis />}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Dashboard
