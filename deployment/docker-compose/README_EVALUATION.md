# Daily Model Evaluation with Opik

## Overview
This setup allows you to run daily evaluations of your model using Opik for tracking and visualization.

## What You Get
- ✅ Store test questions in Opik datasets
- ✅ Run evaluations against your model API (with bearer token)
- ✅ Track metrics over time
- ✅ View results in Opik UI
- ✅ Compare performance across days

## Setup Instructions

### 1. Install Opik SDK
```bash
pip install opik
```

### 2. Configure Environment Variables
```bash
export OPIK_URL="http://localhost:5173/api"
export MODEL_URL="https://your-model-api.com/v1/chat/completions"
export MODEL_BEARER_TOKEN="your-bearer-token-here"
```

### 3. Test the Evaluation Script
```bash
python3 evaluation_script.py
```

### 4. Schedule Daily Runs

#### Option A: Using Cron (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM
0 9 * * * /path/to/schedule_evaluation.sh
```

#### Option B: Using GitHub Actions
Create `.github/workflows/daily-evaluation.yml`:
```yaml
name: Daily Model Evaluation

on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM daily
  workflow_dispatch:  # Allow manual trigger

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install opik requests
      
      - name: Run evaluation
        env:
          OPIK_URL: ${{ secrets.OPIK_URL }}
          MODEL_URL: ${{ secrets.MODEL_URL }}
          MODEL_BEARER_TOKEN: ${{ secrets.MODEL_BEARER_TOKEN }}
        run: python evaluation_script.py
```

#### Option C: Using Docker Compose Service
Add to your `docker-compose.yaml`:
```yaml
  daily-evaluator:
    image: python:3.11-slim
    volumes:
      - ./evaluation_script.py:/app/evaluation_script.py
    environment:
      - OPIK_URL=http://frontend:5173/api
      - MODEL_URL=${MODEL_URL}
      - MODEL_BEARER_TOKEN=${MODEL_BEARER_TOKEN}
    command: |
      sh -c "
        pip install opik requests &&
        while true; do
          python /app/evaluation_script.py
          sleep 86400  # 24 hours
        done
      "
    depends_on:
      - frontend
      - backend
```

#### Option D: Using Airflow
```python
# airflow_dag.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 12, 25),
    'email_on_failure': True,
    'email': ['team@example.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_model_evaluation',
    default_args=default_args,
    description='Daily model evaluation with Opik',
    schedule_interval='0 9 * * *',  # 9 AM daily
    catchup=False,
)

run_evaluation = BashOperator(
    task_id='run_evaluation',
    bash_command='/path/to/schedule_evaluation.sh',
    dag=dag,
)
```

## Customization

### Adding Custom Metrics
```python
from opik.evaluation.metrics import base_metric

class CustomMetric(base_metric.BaseMetric):
    def __init__(self, name="custom"):
        super().__init__(name=name)
    
    def score(self, output: str, expected: str = None, **kwargs):
        # Your custom scoring logic
        return 1.0 if "keyword" in output else 0.0

# Use in evaluation
metrics = [CustomMetric(), Equals(), LevenshteinRatio()]
```

### Using Multiple Models
```python
models = [
    {"name": "model-v1", "url": "https://api1.com", "token": "token1"},
    {"name": "model-v2", "url": "https://api2.com", "token": "token2"},
]

for model in models:
    results = evaluate(
        experiment_name=f"daily-eval-{model['name']}",
        dataset=dataset,
        task=lambda x: call_model(x, model),
        scoring_metrics=metrics,
    )
```

## View Results

1. Open Opik UI: http://localhost:5173
2. Navigate to "Experiments"
3. Compare results across days
4. Create dashboards and alerts

## Architecture

```
┌─────────────────┐
│  Your Scheduler │  (Cron/GitHub Actions/Airflow)
│   (Daily Run)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Evaluation     │  evaluation_script.py
│  Script         │  - Loads test questions
└────────┬────────┘  - Calls your model API
         │           - Computes metrics
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐  ┌──────────┐
│ Model  │  │  Opik    │
│  API   │  │ (Stores  │
│ (with  │  │ results) │
│ Bearer │  │          │
│ Token) │  │          │
└────────┘  └──────────┘
```

## Troubleshooting

### Authentication Issues
- Verify your bearer token is valid
- Check if token needs refresh
- Ensure MODEL_URL is correct

### Network Issues (Docker)
If running evaluation from outside Docker and Opik inside:
```bash
# Use host networking or exposed ports
export OPIK_URL="http://localhost:5173/api"
```

If running evaluation inside Docker:
```bash
# Use service names
export OPIK_URL="http://frontend:5173/api"
```

## Next Steps

1. ✅ Set up your test questions dataset
2. ✅ Configure model API credentials
3. ✅ Run test evaluation manually
4. ✅ Set up scheduling
5. ✅ Create dashboards in Opik UI
6. 📊 Monitor trends over time
7. 🔔 Set up alerts for metric degradation
