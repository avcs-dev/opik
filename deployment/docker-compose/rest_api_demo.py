#!/usr/bin/env python3
"""
REST API Demo - Track Quality Without SDK
Use Opik's REST API directly if SDK installation is problematic
"""

import requests
import json
from datetime import datetime

OPIK_URL = "http://localhost:5173/api"

def check_opik_health():
    """Check if Opik is running"""
    try:
        response = requests.get(f"{OPIK_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def create_experiment_via_api(experiment_name, scores):
    """
    Track quality metrics using Opik REST API
    
    Args:
        experiment_name: Name of the experiment
        scores: Dict of metric names to values
    """
    
    # Example API calls to track experiments
    # Note: Actual API endpoints may vary - check Opik API docs
    
    print(f"📊 Tracking experiment: {experiment_name}")
    print(f"📈 Scores: {json.dumps(scores, indent=2)}")
    
    # You can make direct API calls here
    # For example:
    # response = requests.post(
    #     f"{OPIK_URL}/v1/private/experiments",
    #     json={
    #         "name": experiment_name,
    #         "metrics": scores,
    #         "timestamp": datetime.now().isoformat()
    #     }
    # )
    
    return True

def main():
    print("\n" + "="*60)
    print("OPIK QUALITY TRACKING - REST API DEMO")
    print("="*60 + "\n")
    
    print("🔍 Checking Opik status...")
    if check_opik_health():
        print("✅ Opik is running!\n")
    else:
        print("❌ Opik is not accessible at http://localhost:5173")
        print("   Start it with: docker compose up -d\n")
        return
    
    # Simulate quality tracking
    experiment_name = f"quality-eval-{datetime.now().strftime('%Y%m%d-%H%M')}"
    
    scores = {
        "overall_quality": 0.89,
        "relevance": 0.92,
        "accuracy": 0.87,
        "conciseness": 0.85,
        "user_satisfaction": 0.84,
    }
    
    create_experiment_via_api(experiment_name, scores)
    
    print("\n" + "="*60)
    print("VIEW YOUR TRENDS")
    print("="*60 + "\n")
    
    print("🌐 Open Opik UI: http://localhost:5173\n")
    
    print("What you can do in the UI:")
    print("  1. View all experiments and their metrics")
    print("  2. Compare experiments side-by-side")
    print("  3. See trend charts over time")
    print("  4. Filter by date range or category")
    print("  5. Export data for further analysis\n")
    
    print("="*60)
    print("QUALITY TREND EXAMPLES")
    print("="*60 + "\n")
    
    print("Week-over-Week Comparison:")
    print("─" * 60)
    print(f"{'Metric':<20} {'This Week':<12} {'Last Week':<12} {'Change':>12}")
    print("─" * 60)
    print(f"{'Quality':<20} {0.89:<12.2f} {0.86:<12.2f} {'↑ +3%':>12}")
    print(f"{'Relevance':<20} {0.92:<12.2f} {0.87:<12.2f} {'↑ +5%':>12}")
    print(f"{'Accuracy':<20} {0.87:<12.2f} {0.89:<12.2f} {'↓ -2%':>12}")
    print(f"{'User Rating':<20} {'4.2⭐':<12} {'4.1⭐':<12} {'↑':>12}")
    print("─" * 60 + "\n")
    
    print("Category Breakdown:")
    print("─" * 60)
    print(f"{'Category':<20} {'Score':<12} {'Bar':>28}")
    print("─" * 60)
    print(f"{'Technical':<20} {0.92:<12.2f} {'█' * 18}")
    print(f"{'Support':<20} {0.85:<12.2f} {'█' * 17}")
    print(f"{'General':<20} {0.78:<12.2f} {'█' * 16}")
    print(f"{'Product':<20} {0.91:<12.2f} {'█' * 18}")
    print("─" * 60 + "\n")
    
    print("✅ Quality tracking demo complete!\n")

if __name__ == "__main__":
    main()
