import { useState } from 'react'
import './RiskAnalysis.css'

function RiskAnalysis() {
  const [riskParams, setRiskParams] = useState({
    rainfall_mm: 50,
    slope_degree: 10,
    historical_incident_count: 2,
    road_age_years: 5,
    road_condition_score: 70
  })

  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)

  const handlePredict = async () => {
    setLoading(true)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/ml/predict-risk`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(riskParams)
      })

      const data = await response.json()
      setPrediction(data)
    } catch (error) {
      console.error('Error predicting risk:', error)
      alert('Error predicting risk. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setRiskParams({
      ...riskParams,
      [e.target.name]: parseFloat(e.target.value)
    })
  }

  const getRiskCategoryColor = (category) => {
    switch(category) {
      case 'high': return '#ef4444'
      case 'medium': return '#f59e0b'
      case 'low': return '#22c55e'
      default: return '#6b7280'
    }
  }

  return (
    <div className="risk-analysis">
      <div className="risk-header">
        <h2>📊 Risk Prediction Engine</h2>
        <p>ML-based road risk prediction using terrain, weather, and historical data</p>
        <span className="ml-badge">Machine Learning: Random Forest + Rule-based Fallback</span>
      </div>

      <div className="risk-content">
        <div className="risk-input-panel">
          <h3>Risk Parameters</h3>
          <div className="parameter-grid">
            <div className="parameter-item">
              <label htmlFor="rainfall_mm">Rainfall (mm)</label>
              <input
                type="number"
                id="rainfall_mm"
                name="rainfall_mm"
                value={riskParams.rainfall_mm}
                onChange={handleChange}
                min="0"
                max="500"
              />
              <span className="parameter-range">0-500mm</span>
            </div>

            <div className="parameter-item">
              <label htmlFor="slope_degree">Slope (degrees)</label>
              <input
                type="number"
                id="slope_degree"
                name="slope_degree"
                value={riskParams.slope_degree}
                onChange={handleChange}
                min="0"
                max="90"
              />
              <span className="parameter-range">0-90°</span>
            </div>

            <div className="parameter-item">
              <label htmlFor="historical_incident_count">Historical Incidents</label>
              <input
                type="number"
                id="historical_incident_count"
                name="historical_incident_count"
                value={riskParams.historical_incident_count}
                onChange={handleChange}
                min="0"
                max="50"
              />
              <span className="parameter-range">Count</span>
            </div>

            <div className="parameter-item">
              <label htmlFor="road_age_years">Road Age (years)</label>
              <input
                type="number"
                id="road_age_years"
                name="road_age_years"
                value={riskParams.road_age_years}
                onChange={handleChange}
                min="0"
                max="100"
              />
              <span className="parameter-range">0-100 years</span>
            </div>

            <div className="parameter-item">
              <label htmlFor="road_condition_score">Road Condition Score</label>
              <input
                type="number"
                id="road_condition_score"
                name="road_condition_score"
                value={riskParams.road_condition_score}
                onChange={handleChange}
                min="0"
                max="100"
              />
              <span className="parameter-range">0-100 (higher = better)</span>
            </div>
          </div>

          <button 
            className="btn-predict" 
            onClick={handlePredict}
            disabled={loading}
          >
            {loading ? 'Calculating...' : '🔮 Predict Risk'}
          </button>
        </div>

        {prediction && (
          <div className="risk-results-panel">
            <h3>Risk Prediction Results</h3>
            
            <div className="risk-score-display">
              <div 
                className="risk-score-circle"
                style={{ 
                  borderColor: getRiskCategoryColor(prediction.risk_category),
                  color: getRiskCategoryColor(prediction.risk_category)
                }}
              >
                <span className="score-value">{prediction.risk_score}</span>
                <span className="score-label">Risk Score</span>
              </div>
              <div className="risk-category-badge">
                <span 
                  className="category-text"
                  style={{ backgroundColor: getRiskCategoryColor(prediction.risk_category) }}
                >
                  {prediction.risk_category.toUpperCase()} RISK
                </span>
              </div>
            </div>

            <div className="confidence-meter">
              <label>Model Confidence</label>
              <div className="confidence-bar">
                <div 
                  className="confidence-fill"
                  style={{ width: `${prediction.confidence * 100}%` }}
                ></div>
              </div>
              <span className="confidence-value">{(prediction.confidence * 100).toFixed(0)}%</span>
            </div>

            <div className="feature-importance">
              <h4>Feature Importance</h4>
              {Object.entries(prediction.feature_importance).map(([feature, importance]) => (
                <div key={feature} className="importance-item">
                  <span className="feature-name">{feature.replace(/_/g, ' ')}</span>
                  <div className="importance-bar">
                    <div 
                      className="importance-fill"
                      style={{ width: `${importance}%` }}
                    ></div>
                  </div>
                  <span className="importance-value">{importance.toFixed(1)}%</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="risk-info">
        <h3>Risk Categories</h3>
        <div className="risk-legend">
          <div className="legend-item high">
            <span className="legend-color"></span>
            <div className="legend-text">
              <h4>High Risk (70-100)</h4>
              <p>Critical conditions, avoid if possible</p>
            </div>
          </div>
          <div className="legend-item medium">
            <span className="legend-color"></span>
            <div className="legend-text">
              <h4>Medium Risk (40-69)</h4>
              <p>Exercise caution, monitor conditions</p>
            </div>
          </div>
          <div className="legend-item low">
            <span className="legend-color"></span>
            <div className="legend-text">
              <h4>Low Risk (0-39)</h4>
              <p>Normal conditions, safe for travel</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RiskAnalysis
