#!/bin/bash
echo "=== Starting Socrates Web App ==="
echo "1. Activating Python virtual environment..."
source /Users/jaychauhan/mlx_env/bin/activate

echo "2. Opening browser to http://127.0.0.1:8080..."
# Wait a brief moment after starting the server before opening, or open immediately
(sleep 2 && open http://127.0.0.1:8080) &

echo "3. Launching FastAPI server (loading MLX model, please wait)..."
python3 /Users/jaychauhan/socrates_app/server.py
