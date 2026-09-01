"""
SIH26002 Demo Scenario Script
This script demonstrates the end-to-end workflow of the platform
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def demo_scenario():
    print_section("SIH26002 - End-to-End Demo Scenario")
    
    print("This demo simulates the complete workflow:")
    print("1. Field officer reports a landslide incident")
    print("2. Risk engine recalculates road risk")
    print("3. Routing engine calculates safer alternate route")
    print("4. Medicine vehicle switches to safer route")
    print("5. System generates multilingual alert")
    
    input("\nPress Enter to start the demo...")
    
    # Step 1: Check dashboard summary
    print_section("Step 1: Initial Dashboard Status")
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard/summary")
        if response.status_code == 200:
            data = response.json()
            print("Initial Dashboard Status:")
            print(json.dumps(data, indent=2))
        else:
            print("Error fetching dashboard summary")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the backend server is running on http://localhost:8000")
        return
    
    time.sleep(2)
    
    # Step 2: Report new incident
    print_section("Step 2: Field Officer Reports Landslide Incident")
    incident_data = {
        "incident_type": "landslide",
        "description": "Major landslide on NH-44 near Shillong blocking traffic",
        "latitude": 25.60,
        "longitude": 91.90,
        "severity": "high",
        "photo_url": None
    }
    
    print("Reporting incident:")
    print(json.dumps(incident_data, indent=2))
    
    try:
        response = requests.post(f"{BASE_URL}/api/incidents/report", json=incident_data)
        if response.status_code == 200:
            incident = response.json()
            print(f"\n✓ Incident reported successfully!")
            print(f"  Incident ID: {incident['id']}")
            print(f"  Type: {incident['incident_type']}")
            print(f"  Severity: {incident['severity']}")
        else:
            print(f"Error reporting incident: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(2)
    
    # Step 3: Predict risk for affected road
    print_section("Step 3: ML Risk Prediction for Affected Road")
    risk_params = {
        "rainfall_mm": 150.0,
        "slope_degree": 25.0,
        "historical_incident_count": 5,
        "road_age_years": 15,
        "road_condition_score": 40.0
    }
    
    print("Risk prediction parameters:")
    print(json.dumps(risk_params, indent=2))
    
    try:
        response = requests.post(f"{BASE_URL}/api/ml/predict-risk", json=risk_params)
        if response.status_code == 200:
            prediction = response.json()
            print(f"\nRisk Prediction Results:")
            print(f"  Risk Score: {prediction['risk_score']}/100")
            print(f"  Risk Category: {prediction['risk_category'].upper()}")
            print(f"  Confidence: {prediction['confidence']*100:.0f}%")
            print(f"\n  Feature Importance:")
            for feature, importance in prediction['feature_importance'].items():
                print(f"    {feature}: {importance:.1f}%")
        else:
            print(f"Error predicting risk: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(2)
    
    # Step 4: Get alternate route
    print_section("Step 4: Calculate Safer Alternate Route")
    route_params = {
        "from_lat": 25.58,
        "from_lon": 91.89,
        "to_lat": 26.14,
        "to_lon": 91.73
    }
    
    print("Route calculation parameters:")
    print(json.dumps(route_params, indent=2))
    
    try:
        response = requests.get(f"{BASE_URL}/api/routes/alternate", params=route_params)
        if response.status_code == 200:
            route = response.json()
            print(f"\nSafest Alternate Route:")
            print(f"  Route Type: {route['route_type']}")
            print(f"  Distance: {route['distance_km']} km")
            print(f"  Estimated Time: {route['estimated_time_minutes']} minutes")
            print(f"  Risk Score: {route['risk_score']}/100")
            print(f"  Waypoints: {len(route['waypoints'])} points")
        else:
            print(f"Error calculating route: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(2)
    
    # Step 5: Track vehicle
    print_section("Step 5: Track Medicine Vehicle")
    try:
        response = requests.get(f"{BASE_URL}/api/vehicles/VEH-001/track")
        if response.status_code == 200:
            vehicle = response.json()
            print(f"Vehicle Tracking - VEH-001:")
            print(f"  Cargo Type: {vehicle['cargo_type']}")
            print(f"  Current Position: {vehicle['current_position']['lat']:.4f}, {vehicle['current_position']['lon']:.4f}")
            print(f"  Destination: {vehicle['destination']['lat']:.4f}, {vehicle['destination']['lon']:.4f}")
            print(f"  Status: {vehicle['status'].upper()}")
            print(f"  ETA: {vehicle['eta_minutes']} minutes")
            print(f"  Route Risk: {vehicle['route_risk_score']}/100")
            print(f"\n  Note: Vehicle has been rerouted to safer alternate route")
        else:
            print(f"Error tracking vehicle: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(2)
    
    # Step 6: Broadcast alert
    print_section("Step 6: Broadcast Multilingual Alert")
    alert_data = {
        "severity": "high",
        "message": "HIGH RISK ALERT: NH-44 Shillong to Guwahati - Major landslide reported. Use alternate route via NH-37. Traffic diverted.",
        "language": "en"
    }
    
    print("Broadcasting alert:")
    print(json.dumps(alert_data, indent=2))
    
    try:
        response = requests.post(f"{BASE_URL}/api/alerts/broadcast", json=alert_data)
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ Alert broadcast successfully!")
            print(f"  Alert ID: {result['alert_id']}")
        else:
            print(f"Error broadcasting alert: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(2)
    
    # Step 7: Final dashboard status
    print_section("Step 7: Updated Dashboard Status")
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard/summary")
        if response.status_code == 200:
            data = response.json()
            print("Updated Dashboard Status:")
            print(json.dumps(data, indent=2))
        else:
            print("Error fetching dashboard summary")
    except Exception as e:
        print(f"Error: {e}")
    
    print_section("Demo Scenario Completed")
    print("The end-to-end workflow has been demonstrated successfully!")
    print("\nKey Features Shown:")
    print("✓ Incident reporting with GPS coordinates")
    print("✓ ML-based risk prediction with feature importance")
    print("✓ Safer alternate route calculation")
    print("✓ Real-time vehicle tracking with route updates")
    print("✓ Multilingual alert broadcasting")
    print("✓ Dashboard statistics and monitoring")

if __name__ == "__main__":
    print("SIH26002 Demo Scenario")
    print("======================")
    print("\nPrerequisites:")
    print("- Backend server must be running on http://localhost:8000")
    print("- Database must be seeded with demo data")
    print("\nStarting demo...\n")
    
    demo_scenario()
