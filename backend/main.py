from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# Import routers
from routers import auth, incidents, districts, routes, vehicles, alerts, ml, dashboard

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting SIH26002 Backend...")
    yield
    # Shutdown
    print("Shutting down SIH26002 Backend...")

app = FastAPI(
    title="SIH26002 - AI-Based Smart Logistics & Accessibility Intelligence Platform",
    description="Decision-support platform for North Eastern Region (NER) combining road accessibility, route disruption risk prediction, and logistics intelligence",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(incidents.router, prefix="/api/incidents", tags=["Incidents"])
app.include_router(districts.router, prefix="/api/districts", tags=["Districts"])
app.include_router(routes.router, prefix="/api/routes", tags=["Routes"])
app.include_router(vehicles.router, prefix="/api/vehicles", tags=["Vehicles"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(ml.router, prefix="/api/ml", tags=["ML"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

@app.get("/")
async def root():
    return {
        "message": "SIH26002 - AI-Based Smart Logistics & Accessibility Intelligence Platform",
        "version": "1.0.0",
        "status": "Prototype - Simulated Data"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
