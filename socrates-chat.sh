#!/bin/bash
echo "Launching Socrates 14B (DPO) Chat CLI..."
source /Users/jaychauhan/mlx_env/bin/activate
mlx_lm.chat \
  --model /Users/jaychauhan/socrates-qwen2.5-14b-dpo-mlx-q4 \
  --system-prompt "You are simulating a survey respondent. Answer exactly as instructed, following the specified response format without additional commentary."
