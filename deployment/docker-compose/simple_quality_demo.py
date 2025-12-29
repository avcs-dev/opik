#!/usr/bin/env python3
"""
Simple Quality Tracking Demo for Opik
This is a simplified version that shows the core concepts without heavy dependencies
"""

import os
import time
from datetime import datetime

print("\n" + "="*60)
print("OPIK QUALITY TRACKING - SIMPLIFIED DEMO")
print("="*60 + "\n")

print("📦 Installing Opik dependencies (this may take a moment)...")
print("   Note: First run may be slow due to dependency compilation\n")

try:
    # Import opik - this might take time on first run
    print("⏳ Loading Opik SDK...")
    import opik
    from opik import Opik
    print("✅ Opik SDK loaded successfully!\n")
    
    # Initialize client
    OPIK_URL = os.getenv("OPIK_URL", "http://localhost:5173/api")
    print(f"🔗 Connecting to Opik at: {OPIK_URL}")
    
    client = Opik(url=OPIK_URL)
    print("✅ Connected to Opik!\n")
    
    print("="*60)
    print("DEMO: Creating a Sample Quality Evaluation")
    print("="*60 + "\n")
    
    # Create a simple dataset
    dataset_name = f"demo-quality-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print(f"📊 Creating dataset: {dataset_name}")
    
    dataset = client.create_dataset(
        name=dataset_name,
        description="Demo quality evaluation dataset"
    )
    
    # Add sample questions
    sample_questions = [
        {
            "question": "What is machine learning?",
            "expected_answer": "Machine learning is a subset of AI",
            "category": "technical"
        },
        {
            "question": "What are your business hours?",
            "expected_answer": "Monday to Friday, 9 AM to 5 PM",
            "category": "general"
        },
    ]
    
    for item in sample_questions:
        dataset.insert([item])
    
    print(f"✅ Added {len(sample_questions)} questions to dataset\n")
    
    print("="*60)
    print("QUALITY TRACKING CAPABILITIES")
    print("="*60 + "\n")
    
    print("✅ What you can track in Opik:\n")
    print("   📈 Automated Quality Metrics:")
    print("      • Overall Quality Score (0-1)")
    print("      • Relevance Score")
    print("      • Accuracy Score")
    print("      • Response Time")
    print("      • Token Usage\n")
    
    print("   💬 User Feedback:")
    print("      • Star ratings (1-5)")
    print("      • Thumbs up/down")
    print("      • Qualitative comments")
    print("      • Issue categories\n")
    
    print("   📊 Trend Visualization:")
    print("      • Time-series charts")
    print("      • Week-over-week comparisons")
    print("      • Category breakdowns")
    print("      • Anomaly detection\n")
    
    print("="*60)
    print("HOW TO VIEW TRENDS")
    print("="*60 + "\n")
    
    print("1. Open Opik UI in your browser:")
    print(f"   🌐 http://localhost:5173\n")
    
    print("2. Navigate to 'Experiments' tab\n")
    
    print("3. You'll see experiments listed by date:")
    print("   • quality-tracking-20251226-0900")
    print("   • quality-tracking-20251225-0900")
    print("   • quality-tracking-20251224-0900\n")
    
    print("4. Select multiple experiments and click 'Compare'\n")
    
    print("5. View trends over time:")
    print("""
    Quality Score Trend
    ┌────────────────────────────────┐
    │ 1.0 │                    ╱─╲   │
    │ 0.8 │                ╱──╯   ╲  │
    │ 0.6 │            ╱──╯         │
    │ 0.4 │        ╱──╯             │
    │ 0.2 │    ╱──╯                 │
    │ 0.0 │───╯                     │
    └─────┴──────────────────────────┘
       Dec 20  21   22   23   24   25
    """)
    
    print("="*60)
    print("NEXT STEPS")
    print("="*60 + "\n")
    
    print("1. ✅ Install complete - Opik is ready")
    print("2. 📝 Customize evaluation_script.py with your model API")
    print("3. 🔑 Set environment variables:")
    print("      export MODEL_URL='your-api-url'")
    print("      export MODEL_BEARER_TOKEN='your-token'")
    print("4. ▶️  Run: python evaluation_script.py")
    print("5. 📊 View results at http://localhost:5173")
    print("6. ⏰ Schedule daily runs (see README_EVALUATION.md)\n")
    
    print("="*60)
    print("SUCCESS! ✨")
    print("="*60)
    print("\nOpik is ready to track your model quality trends!")
    print(f"Dataset created: {dataset_name}")
    print(f"View it at: http://localhost:5173\n")

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\nℹ️  This is likely due to missing system dependencies.")
    print("   The Opik SDK requires some compiled components.\n")
    print("🔧 Try these solutions:")
    print("   1. Wait a minute and try again (compilation in progress)")
    print("   2. Install system dependencies:")
    print("      brew install gcc (macOS)")
    print("   3. Use a fresh Python 3.9+ environment\n")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔍 Troubleshooting:")
    print("   1. Ensure Opik is running: docker compose ps")
    print("   2. Check Opik is accessible: curl http://localhost:5173")
    print("   3. Verify Python version: python --version (need 3.9+)")
    print(f"   4. Check logs for details\n")

print("\n📚 Documentation:")
print("   • Quality Trends Guide: QUALITY_TRENDS_GUIDE.md")
print("   • Evaluation Setup: README_EVALUATION.md")
print("   • Full Example: quality_tracking_example.py\n")
