# 📊 Tracking Answer Quality Trends in Opik

## Overview
Opik provides comprehensive tools to track and visualize answer quality trends over time, helping you monitor model performance and identify degradation or improvements.

## 🎯 What You Can Track

### 1. **Automated Quality Metrics**
Track these metrics automatically on every evaluation run:

- **Overall Quality Score** (0-1) - Composite quality measure
- **Relevance Score** (0-1) - How well the answer addresses the question
- **Accuracy Score** (0-1) - Factual correctness vs ground truth
- **Conciseness Score** (0-1) - Appropriate length and clarity
- **Similarity Score** (0-1) - Closeness to expected answer

### 2. **User Feedback Metrics**
Collect and trend real user feedback:

- ⭐ Star ratings (1-5)
- 👍👎 Thumbs up/down
- 💬 Qualitative feedback
- 🏷️ Issue categories (accuracy, relevance, tone, etc.)

### 3. **Performance Metrics**
Monitor operational aspects:

- ⏱️ Response latency
- 🔄 Retry rates
- ❌ Error rates
- 💰 Token usage / costs

## 📈 How to View Trends in Opik UI

### Method 1: Experiments Dashboard

1. **Open Opik UI**: http://localhost:5173
2. **Navigate to Experiments** tab
3. **View Options**:
   ```
   ┌─────────────────────────────────────────┐
   │  Experiments                            │
   ├─────────────────────────────────────────┤
   │  ✓ quality-tracking-20251225-0900       │
   │  ✓ quality-tracking-20251224-0900       │
   │  ✓ quality-tracking-20251223-0900       │
   │                                         │
   │  [Compare Selected]  [Export]           │
   └─────────────────────────────────────────┘
   ```

4. **Compare Multiple Experiments**:
   - Select 2+ experiments
   - Click "Compare"
   - View side-by-side metric comparisons

### Method 2: Time Series View

1. Navigate to **Analytics** section
2. Select metrics to visualize
3. Choose date range
4. View trends:
   ```
   Quality Score Over Time
   ┌────────────────────────────────┐
   │ 1.0 │                    ╱─╲   │
   │ 0.8 │                ╱──╯   ╲  │
   │ 0.6 │            ╱──╯         │
   │ 0.4 │        ╱──╯             │
   │ 0.2 │    ╱──╯                 │
   │ 0.0 │───╯                     │
   └─────┴──────────────────────────┘
      Dec 20  21   22   23   24   25
   ```

### Method 3: Category-Based Analysis

Track quality by question category:
```
Technical Questions:    0.92 ████████████░░
Support Questions:      0.85 █████████████░
General Questions:      0.78 ████████████░░
Product Questions:      0.91 █████████████░
```

## 🔧 Implementation Example

### Basic Setup
```python
from opik.evaluation.metrics import base_metric

class QualityScore(base_metric.BaseMetric):
    def score(self, output: str, expected: str = None):
        # Your quality assessment logic
        return quality_value  # 0.0 to 1.0

# Run daily and track over time
results = evaluate(
    experiment_name=f"quality-{date}",
    task=your_task,
    scoring_metrics=[QualityScore()],
)
```

### With User Feedback
```python
from opik import Opik

client = Opik()

# When user rates an answer
client.log_traces_feedback_scores(
    project_name="my-project",
    scores=[{
        "trace_id": trace_id,
        "name": "user_satisfaction",
        "value": rating / 5.0,  # 1-5 stars normalized
        "reason": user_comment,
    }]
)
```

## 📊 Dashboard Examples

### Quality Scorecard Dashboard
Create a custom dashboard showing:

```
┌─────────────────────────────────────────────────────┐
│  Quality Metrics - Last 7 Days                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Overall Quality:        0.89  ↑ +0.03             │
│  Relevance:             0.92  ↑ +0.05             │
│  Accuracy:              0.87  ↓ -0.02  ⚠️          │
│  Conciseness:           0.85  → +0.00             │
│  User Satisfaction:     4.2/5  ↑ +0.1             │
│                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                     │
│  Alerts:                                           │
│  ⚠️  Accuracy dropped 2% - investigate tech Q's    │
│  ✅  Relevance improved - model update working     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Trend Comparison Dashboard
```
┌─────────────────────────────────────────────────────┐
│  Week-over-Week Comparison                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Metric            This Week   Last Week   Change  │
│  ──────────────────────────────────────────────────│
│  Quality           0.89        0.86        ↑ +3%   │
│  Relevance         0.92        0.87        ↑ +5%   │
│  Accuracy          0.87        0.89        ↓ -2%   │
│  Response Time     245ms       312ms       ↑ +21%  │
│  User Rating       4.2⭐       4.1⭐        ↑       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🔔 Setting Up Alerts

### Option 1: Using Opik API
```python
def check_quality_degradation():
    # Get recent experiments
    recent_scores = get_recent_scores(days=7)
    
    if recent_scores['quality'] < 0.80:  # Threshold
        send_alert(
            title="Quality Score Below Threshold",
            message=f"Current: {recent_scores['quality']:.2f}",
            severity="warning"
        )
```

### Option 2: Using Monitoring Tools
Integrate with tools like:
- **Grafana** - Real-time dashboards
- **Datadog** - APM monitoring
- **PagerDuty** - Alert management
- **Slack** - Team notifications

### Option 3: Email Notifications
```python
def send_quality_report(frequency='daily'):
    results = get_latest_evaluation()
    
    if results.quality_score < previous_score * 0.95:  # 5% drop
        send_email(
            to="team@company.com",
            subject="⚠️ Quality Alert: Performance Degradation",
            body=generate_report(results)
        )
```

## 📈 Advanced Analytics

### 1. Statistical Analysis
```python
import pandas as pd

# Export Opik data to DataFrame
experiments_df = pd.DataFrame([
    {
        'date': exp.date,
        'quality': exp.scores['quality'],
        'relevance': exp.scores['relevance'],
    }
    for exp in get_all_experiments()
])

# Calculate trends
experiments_df['quality_ma'] = experiments_df['quality'].rolling(7).mean()
experiments_df['quality_std'] = experiments_df['quality'].rolling(7).std()

# Detect anomalies
anomalies = experiments_df[
    (experiments_df['quality'] < experiments_df['quality_ma'] - 2 * experiments_df['quality_std'])
]
```

### 2. Correlation Analysis
```python
# Find correlations between metrics
correlation_matrix = experiments_df[['quality', 'relevance', 'conciseness']].corr()

# Example: If relevance drops, quality often drops too
if correlation_matrix.loc['relevance', 'quality'] > 0.7:
    print("High correlation: Focus on improving relevance")
```

### 3. Category Performance
```python
# Track quality by question category
category_trends = {
    'technical': experiments_df[experiments_df['category'] == 'technical']['quality'].mean(),
    'support': experiments_df[experiments_df['category'] == 'support']['quality'].mean(),
    'general': experiments_df[experiments_df['category'] == 'general']['quality'].mean(),
}

# Identify weak areas
weakest = min(category_trends, key=category_trends.get)
print(f"Focus improvement efforts on: {weakest}")
```

## 🎯 Best Practices

### 1. **Consistent Evaluation Schedule**
```bash
# Run at the same time daily
0 9 * * * /path/to/quality_tracking_example.py
```

### 2. **Version Everything**
Track model versions, prompts, and configs:
```python
experiment_config={
    "model_version": "gpt-4-2024-01",
    "prompt_version": "v2.3",
    "temperature": 0.7,
    "git_commit": get_git_commit(),
}
```

### 3. **Use Multiple Metrics**
Don't rely on a single metric:
- Automated scores (objective)
- User feedback (subjective)
- Business KPIs (e.g., resolution rate)

### 4. **Set Appropriate Thresholds**
```python
thresholds = {
    'quality': 0.80,      # Minimum acceptable
    'relevance': 0.85,
    'user_rating': 4.0,
}
```

### 5. **Regular Reviews**
- **Daily**: Automated checks
- **Weekly**: Team review of trends
- **Monthly**: Deep dive analysis

## 🔍 Troubleshooting Quality Issues

When you notice quality degradation:

1. **Check Recent Changes**
   - Model version updates?
   - Prompt changes?
   - New data sources?

2. **Drill Down by Category**
   - Which question types are affected?
   - Is it specific to certain topics?

3. **Review Individual Cases**
   - Look at low-scoring examples
   - Identify patterns in failures

4. **Compare with Baseline**
   - Use Opik's comparison view
   - Look at before/after metrics

## 📚 Resources

- **Opik Documentation**: https://github.com/comet-ml/opik
- **Evaluation Guide**: See `evaluation_script.py`
- **Custom Metrics**: See `quality_tracking_example.py`
- **API Reference**: http://localhost:5173/api/docs

## 🚀 Getting Started

1. Run the quality tracking script:
   ```bash
   python quality_tracking_example.py
   ```

2. View results in Opik UI:
   ```bash
   open http://localhost:5173
   ```

3. Set up daily runs:
   ```bash
   # Add to crontab
   0 9 * * * /path/to/quality_tracking_example.py
   ```

4. Create your dashboard and start tracking! 📊
