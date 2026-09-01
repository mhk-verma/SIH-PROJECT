# SIH26002 - AI-Based Smart Logistics & Accessibility Intelligence Platform

**Smart India Hackathon 2026 - Problem Statement SIH26002**

A decision-support web platform for North Eastern Region (NER) that combines road accessibility status, route-disruption risk prediction, geo-tagged field incident reporting, safer alternate-route suggestions, simulated essential-goods vehicle tracking, multilingual alerts, and offline-first field reporting.

## 🎯 Problem Statement

**WHAT is disrupted, WHERE is it disrupted, HOW risky is it, WHICH safer route should be used, and WHO needs to be alerted?**

The platform helps answer these questions for logistics operations in NER by providing:
- Real-time road risk assessment
- Safer alternate route suggestions
- Field incident reporting with offline sync
- Essential goods vehicle tracking
- Multilingual alert system

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI (Python) - REST API framework
- SQLAlchemy - ORM for database operations
- SQLite - Database (PostgreSQL + PostGIS ready for production)
- NetworkX - Graph routing algorithms
- JWT - Authentication

**Frontend:**
- React.js + Vite - Modern frontend framework
- Leaflet.js - Interactive maps
- Tailwind CSS - Styling (ready for integration)
- Axios - HTTP client

**ML Engine:**
- Rule-based risk prediction (MVP)
- Ready for Random Forest integration

## 📁 Project Structure

```
SIH/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── seed_data.py         # Database seeding script
│   ├── requirements.txt     # Python dependencies
│   ├── .env                # Environment variables
│   └── routers/            # API endpoints
│       ├── auth.py         # Authentication endpoints
│       ├── incidents.py    # Incident reporting
│       ├── districts.py    # District management
│       ├── routes.py       # Route calculation
│       ├── vehicles.py     # Vehicle tracking
│       ├── alerts.py       # Alert system
│       ├── ml.py           # ML risk prediction
│       └── dashboard.py    # Dashboard statistics
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Global styles
│   │   └── components/     # React components
│   │       ├── Dashboard.jsx
│   │       ├── MapView.jsx
│   │       ├── IncidentReport.jsx
│   │       ├── VehicleTracking.jsx
│   │       ├── AlertsPanel.jsx
│   │       └── RiskAnalysis.jsx
│   └── package.json        # Node dependencies
├── docs/                   # Documentation
└── README.md              # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   # .env file is already configured with SQLite
   # For production, update DATABASE_URL to PostgreSQL
   ```

4. **Seed the database:**
   ```bash
   python seed_data.py
   ```

5. **Start the backend server:**
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:8000`

6. **Access API documentation:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Incidents
- `POST /api/incidents/report` - Report new incident
- `GET /api/incidents/` - Get all incidents
- `GET /api/incidents/{id}` - Get specific incident
- `PATCH /api/incidents/{id}/verify` - Verify incident

### Districts
- `GET /api/districts/` - Get all districts
- `GET /api/districts/{id}` - Get specific district
- `GET /api/districts/{id}/status` - Get district status

### Routes
- `GET /api/routes/alternate` - Get safest alternate route
- `GET /api/routes/shortest` - Get shortest route

### Vehicles
- `GET /api/vehicles/` - Get all vehicles
- `GET /api/vehicles/{id}` - Get specific vehicle
- `GET /api/vehicles/{id}/track` - Track vehicle location

### Alerts
- `POST /api/alerts/broadcast` - Broadcast new alert
- `GET /api/alerts/` - Get all alerts

### ML
- `POST /api/ml/predict-risk` - Predict road risk
- `GET /api/ml/model-info` - Get model information

### Dashboard
- `GET /api/dashboard/summary` - Get dashboard statistics
- `GET /api/dashboard/recent-incidents` - Get recent incidents
- `GET /api/dashboard/high-risk-roads` - Get high-risk roads

## 👥 User Roles

1. **Admin** - Full system access
2. **Field Officer** - Report/verify incidents
3. **Transporter** - Monitor vehicles/routes/alerts
4. **Citizen** - Submit reports/view public alerts

## 🎨 Frontend Features

### Dashboard
- Overview statistics (districts, roads, incidents, vehicles)
- Risk distribution charts
- Road status indicators

### GIS Map
- Interactive map of NER region
- District risk visualization
- Road segment risk coloring
- Incident markers
- Vehicle tracking markers
- Risk legend

### Incident Reporting
- Form for reporting incidents
- GPS location capture
- Photo upload support
- Offline-first design
- Recent incidents display

### Vehicle Tracking
- Real-time vehicle positions
- Cargo type indicators
- Status monitoring
- ETA tracking
- Route risk assessment

### Alerts Panel
- Alert broadcasting
- Multilingual support (English + Hindi)
- Severity-based categorization
- Active alerts display

### Risk Analysis
- ML-based risk prediction
- Parameter input forms
- Risk score visualization
- Feature importance display
- Confidence metrics

## 🧪 Demo Data

The system comes pre-seeded with:
- **4 Districts:** Kamrup (Assam), Shillong (Meghalaya), Imphal (Manipur), Guwahati (Assam)
- **4 Road Segments:** Including NH-37, NH-44, NH-2 with varying risk levels
- **4 Users:** admin, field officer, transporter, citizen
- **3 Vehicles:** Carrying medicine, food, agricultural supplies
- **2 Incidents:** Landslide and flood reports
- **2 Alerts:** High and medium priority alerts

**Default Credentials:**
- Admin: `admin` / `admin123`
- Field Officer: `officer1` / `officer123`
- Transporter: `transporter1` / `transporter123`
- Citizen: `citizen1` / `citizen123`

## 🔧 Demo Scenario

### End-to-End Demo Flow

1. **Field Officer Reports Incident**
   - Navigate to "Incident Report" tab
   - Fill incident details (landslide, location, severity)
   - Submit report

2. **Risk Recalculation**
   - System automatically recalculates road risk
   - Road segment risk score updates
   - Risk category changes (if applicable)

3. **Route Recalculation**
   - Navigate to "GIS Map" tab
   - View updated risk visualization
   - System suggests safer alternate routes

4. **Vehicle Route Update**
   - Navigate to "Vehicle Tracking" tab
   - Medicine vehicle switches to safer route
   - ETA and risk metrics update

5. **Alert Generation**
   - Navigate to "Alerts" tab
   - System generates multilingual alert
   - Alert broadcast to relevant stakeholders

## 📝 Important Notes

### Prototype Status
- This is a **hackathon MVP** with simulated data
- Not a production government system
- Uses SQLite for easy setup (PostgreSQL + PostGIS ready for production)
- ML uses rule-based fallback (Random Forest ready for integration)

### Data Integrity
- All data is clearly labeled as "Prototype - Simulated Data"
- Architecture is ready for authorized government data integration
- No claims of real-time government integration

### Limitations
- GPS tracking is simulated (no physical hardware required)
- SMS alerts are mocked (Firebase ready for production)
- Limited to 3-4 sample NER districts for demo
- English + Hindi languages only (architecture ready for regional languages)

## 🚀 Future Scope

- **Production Database:** PostgreSQL + PostGIS integration
- **Advanced ML:** Random Forest model with training data
- **Real GPS:** Physical GPS hardware integration
- **SMS Gateway:** Firebase Cloud Messaging integration
- **More Languages:** Assamese, Khasi, Manipuri, Mizo
- **More Districts:** Full NER coverage
- **Mobile App:** React Native with offline SQLite
- **Real-time Updates:** WebSocket integration

## 📄 License

This project is developed for Smart India Hackathon 2026.

## 👨‍💻 Team

**Team Name:** Code GenX
**Problem Statement:** SIH26002
**Category:** Software - Transportation & Logistics

---

**Note:** This is a prototype demonstration. For production deployment, proper security measures, data validation, and authorized government integrations would be required.
