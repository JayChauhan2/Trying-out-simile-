#!/bin/bash
echo "Launching Socrates 14B (DPO) OpenAI-Compatible API Server..."
echo "API will be available at http://127.0.0.1:8000/v1"
source /Users/jaychauhan/mlx_env/bin/activate
mlx_lm.server --model /Users/jaychauhan/socrates-qwen2.5-14b-dpo-mlx-q4 --port 8000
