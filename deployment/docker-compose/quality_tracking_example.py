#!/usr/bin/env python3
"""
Track Answer Quality Trends Over Time with Opik

This example shows how to track various quality metrics and view trends
"""

import os
from datetime import datetime
from opik import Opik, track
from opik.evaluation import evaluate
from opik.evaluation.metrics import (
    Equals,
    LevenshteinRatio,
    Contains,
    base_metric
)
import requests


# Initialize Opik client
client = Opik(url=os.getenv("OPIK_URL", "http://localhost:5173/api"))


# ============================================================================
# CUSTOM QUALITY METRICS
# ============================================================================

class ResponseQuality(base_metric.BaseMetric):
    """
    Custom metric to assess overall response quality
    Scores: 0.0 to 1.0
    """
    def __init__(self, name="response_quality"):
        super().__init__(name=name)
    
    def score(self, output: str, reference: str = None, **kwargs):
        score = 0.0
        
        # Check completeness (not too short)
        if len(output) > 50:
            score += 0.25
        
        # Check if it addresses the question
        if reference and any(word.lower() in output.lower() for word in reference.split()):
            score += 0.25
        
        # Check for coherence (basic sentence structure)
        if output.count('.') >= 1 and output.count(' ') >= 5:
            score += 0.25
        
        # Check for proper capitalization
        if output and output[0].isupper():
            score += 0.25
        
        return score


class Relevance(base_metric.BaseMetric):
    """
    Measure how relevant the answer is to the question
    """
    def __init__(self, name="relevance"):
        super().__init__(name=name)
    
    def score(self, output: str, input: str = None, **kwargs):
        if not input:
            return 0.0
        
        # Extract keywords from question
        question_words = set(input.lower().split())
        answer_words = set(output.lower().split())
        
        # Calculate overlap
        common_words = question_words.intersection(answer_words)
        relevance_score = len(common_words) / len(question_words) if question_words else 0.0
        
        return min(relevance_score, 1.0)


class Conciseness(base_metric.BaseMetric):
    """
    Measure if the answer is appropriately concise (not too verbose)
    """
    def __init__(self, name="conciseness", ideal_length=200):
        super().__init__(name=name)
        self.ideal_length = ideal_length
    
    def score(self, output: str, **kwargs):
        length = len(output)
        
        # Score based on distance from ideal length
        if length <= self.ideal_length:
            return 1.0
        else:
            # Penalize verbosity
            excess = length - self.ideal_length
            penalty = min(excess / self.ideal_length, 1.0)
            return max(0.0, 1.0 - penalty)


class Accuracy(base_metric.BaseMetric):
    """
    Measure factual accuracy (if you have ground truth)
    """
    def __init__(self, name="accuracy"):
        super().__init__(name=name)
    
    def score(self, output: str, expected_answer: str = None, **kwargs):
        if not expected_answer:
            return None  # Can't score without ground truth
        
        # Simple keyword-based accuracy
        expected_keywords = expected_answer.lower().split()
        output_lower = output.lower()
        
        matches = sum(1 for keyword in expected_keywords if keyword in output_lower)
        return matches / len(expected_keywords) if expected_keywords else 0.0


# ============================================================================
# TRACKING QUALITY OVER TIME
# ============================================================================

@track()
def call_model_with_tracking(question: str, model_url: str, bearer_token: str):
    """
    Call your model and track the interaction in Opik
    """
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7
    }
    
    response = requests.post(model_url, json=payload, headers=headers)
    response.raise_for_status()
    
    answer = response.json()["choices"][0]["message"]["content"]
    
    return {
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().isoformat()
    }


def run_quality_evaluation_with_trends():
    """
    Run evaluation and track quality metrics over time
    """
    print(f"\n{'='*60}")
    print(f"Running Quality Evaluation: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    
    # Your test dataset
    test_questions = [
        {
            "question": "What is machine learning?",
            "expected_answer": "Machine learning is a subset of AI that enables systems to learn from data",
            "category": "technical"
        },
        {
            "question": "How do I reset my password?",
            "expected_answer": "Click forgot password, check your email, and follow the reset link",
            "category": "support"
        },
        {
            "question": "What are your business hours?",
            "expected_answer": "We are open Monday to Friday, 9 AM to 5 PM",
            "category": "general"
        },
    ]
    
    # Create dataset with timestamp
    dataset_name = f"quality-eval-{datetime.now().strftime('%Y-%m-%d')}"
    dataset = client.create_dataset(
        name=dataset_name,
        description="Daily quality evaluation dataset"
    )
    
    for item in test_questions:
        dataset.insert([item])
    
    # Define comprehensive quality metrics
    quality_metrics = [
        ResponseQuality(name="overall_quality"),
        Relevance(name="relevance_score"),
        Conciseness(name="conciseness_score"),
        Accuracy(name="accuracy_score"),
        LevenshteinRatio(name="similarity_to_expected"),
    ]
    
    # Evaluation task
    def eval_task(dataset_item: dict) -> dict:
        question = dataset_item["question"]
        
        # Simulate model call (replace with your actual model)
        # answer = call_model_with_tracking(
        #     question, 
        #     os.getenv("MODEL_URL"), 
        #     os.getenv("MODEL_BEARER_TOKEN")
        # )["answer"]
        
        # For demo purposes, using a mock answer
        answer = f"This is a sample answer to: {question}"
        
        return {
            "input": question,
            "output": answer,
            "expected_answer": dataset_item.get("expected_answer"),
            "reference": dataset_item.get("expected_answer"),
            "category": dataset_item.get("category"),
        }
    
    # Run evaluation with quality tracking
    experiment_name = f"quality-tracking-{datetime.now().strftime('%Y%m%d-%H%M')}"
    
    results = evaluate(
        experiment_name=experiment_name,
        dataset=dataset,
        task=eval_task,
        scoring_metrics=quality_metrics,
        experiment_config={
            "model_version": "v1.0",
            "evaluation_date": datetime.now().isoformat(),
            "purpose": "quality_monitoring",
        }
    )
    
    print("\n" + "="*60)
    print("Quality Metrics Summary:")
    print("="*60)
    
    # Print summary statistics
    if hasattr(results, 'aggregate_scores'):
        for metric_name, score in results.aggregate_scores.items():
            print(f"  {metric_name}: {score:.3f}")
    
    print("\n✅ Results saved to Opik!")
    print(f"📊 View trends at: http://localhost:5173/experiments")
    print(f"🔍 Experiment name: {experiment_name}")
    
    return results


# ============================================================================
# ANALYZING TRENDS
# ============================================================================

def analyze_quality_trends():
    """
    Fetch and analyze quality trends over time
    """
    print("\n" + "="*60)
    print("Analyzing Quality Trends")
    print("="*60 + "\n")
    
    # Get recent experiments
    # Note: You would typically filter by date range or experiment prefix
    
    print("📈 To view comprehensive trends:")
    print("   1. Open Opik UI: http://localhost:5173")
    print("   2. Navigate to 'Experiments'")
    print("   3. Filter by 'quality-tracking' prefix")
    print("   4. Compare metrics across dates")
    print("   5. Create custom dashboards")
    
    print("\n📊 Trend Analysis Options:")
    print("   • Compare average scores week-over-week")
    print("   • Identify degradation patterns")
    print("   • Spot improvements after model updates")
    print("   • Track by category (technical, support, etc.)")
    print("   • Set up alerts for score drops")


# ============================================================================
# FEEDBACK-BASED QUALITY TRACKING
# ============================================================================

def track_with_user_feedback():
    """
    Example: Track quality using actual user feedback
    """
    from opik import track
    
    @track()
    def handle_user_query(question: str, model_url: str, bearer_token: str):
        # Call model
        answer = "Sample answer"  # Your actual model call here
        
        # Return answer and trace_id for feedback collection
        return answer
    
    # Later, when user provides feedback:
    def collect_user_feedback(trace_id: str, rating: int, feedback_text: str = None):
        """
        Rating: 1-5 stars for answer quality
        """
        client.log_traces_feedback_scores(
            project_name="default",
            scores=[{
                "trace_id": trace_id,
                "name": "user_rating",
                "value": rating / 5.0,  # Normalize to 0-1
                "reason": feedback_text,
            }]
        )
    
    print("💬 User feedback tracking enabled!")
    print("   Collect ratings from users and track quality trends")


if __name__ == "__main__":
    print("\n🎯 OPIK QUALITY TREND TRACKING DEMO\n")
    
    # Run quality evaluation
    results = run_quality_evaluation_with_trends()
    
    # Show how to analyze trends
    analyze_quality_trends()
    
    print("\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    print("1. ✅ Set up daily scheduled runs (see schedule_evaluation.sh)")
    print("2. 📊 View trends in Opik UI")
    print("3. 📈 Create quality dashboards")
    print("4. 🔔 Set up alerts for quality degradation")
    print("5. 💬 Integrate user feedback collection")
    print("\n")
