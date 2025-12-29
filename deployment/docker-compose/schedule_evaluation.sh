#!/bin/bash
# Daily evaluation scheduler script

# Set environment variables
export OPIK_URL="http://localhost:5173/api"
export MODEL_URL="https://your-model-api.com/v1/chat/completions"
export MODEL_BEARER_TOKEN="your-bearer-token-here"

# Optional: Activate virtual environment if using one
# source /path/to/venv/bin/activate

# Run the evaluation script
cd "$(dirname "$0")"
python3 evaluation_script.py

# Log the result
echo "Evaluation completed at $(date)" >> evaluation.log
