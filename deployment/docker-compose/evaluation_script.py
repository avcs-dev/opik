#!/usr/bin/env python3
"""
Daily Model Evaluation Script for Opik
Run your test questions against a model API with bearer token authentication
"""

import os
import opik
from opik import Opik
from opik.evaluation import evaluate
from opik.evaluation.metrics import Contains, Equals, LevenshteinRatio
import requests
from datetime import datetime

# Configuration
OPIK_URL = os.getenv("OPIK_URL", "http://localhost:5173/api")
MODEL_URL = os.getenv("MODEL_URL", "https://your-model-api.com/v1/chat/completions")
MODEL_BEARER_TOKEN = os.getenv("MODEL_BEARER_TOKEN")

# Initialize Opik client
client = Opik(url=OPIK_URL)


def call_your_model(question: str) -> str:
    """
    Call your model API with bearer token authentication
    """
    headers = {
        "Authorization": f"Bearer {MODEL_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7
    }
    
    response = requests.post(MODEL_URL, json=payload, headers=headers)
    response.raise_for_status()
    
    return response.json()["choices"][0]["message"]["content"]


def evaluation_task(dataset_item: dict) -> dict:
    """
    Evaluation task that runs for each question in your dataset
    """
    question = dataset_item["question"]
    
    # Call your model
    answer = call_your_model(question)
    
    return {
        "question": question,
        "output": answer,
        "expected_answer": dataset_item.get("expected_answer"),
        "reference": dataset_item.get("reference")
    }


def run_daily_evaluation():
    """
    Main function to run daily evaluation
    """
    print(f"Starting evaluation run at {datetime.now()}")
    
    # Option 1: Load dataset from Opik
    # dataset = client.get_dataset("my-test-questions")
    
    # Option 2: Define your test questions inline
    test_questions = [
        {
            "question": "What is the capital of France?",
            "expected_answer": "Paris",
        },
        {
            "question": "Explain machine learning in simple terms",
            "expected_answer": None,  # Free-form answer
        },
        {
            "question": "What is 2 + 2?",
            "expected_answer": "4",
        },
        # Add more questions here
    ]
    
    # Create or update dataset in Opik
    dataset = client.create_dataset(
        name=f"daily-eval-{datetime.now().strftime('%Y-%m-%d')}",
        description="Daily evaluation test set"
    )
    
    for item in test_questions:
        dataset.insert([item])
    
    # Define metrics for evaluation
    metrics = [
        Contains(name="contains_keyword"),  # Check if answer contains expected keywords
        Equals(name="exact_match", case_sensitive=False),  # For exact answers
        LevenshteinRatio(name="similarity"),  # Measure similarity
    ]
    
    # Run evaluation
    experiment_config = {
        "model_url": MODEL_URL,
        "timestamp": datetime.now().isoformat(),
    }
    
    results = evaluate(
        experiment_name=f"daily-eval-{datetime.now().strftime('%Y-%m-%d-%H%M')}",
        dataset=dataset,
        task=evaluation_task,
        scoring_metrics=metrics,
        experiment_config=experiment_config,
    )
    
    print(f"Evaluation completed!")
    print(f"Results: {results}")
    print(f"View results in Opik UI: http://localhost:5173")
    
    return results


if __name__ == "__main__":
    try:
        results = run_daily_evaluation()
        print("✅ Evaluation completed successfully")
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        raise
