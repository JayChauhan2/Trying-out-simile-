#!/bin/bash
set -e

echo "=== Starting Socrates LLM Setup ==="
echo "Using virtual environment: /Users/jaychauhan/mlx_env"
source /Users/jaychauhan/mlx_env/bin/activate

# Define paths
MLX_MODEL_PATH="/Users/jaychauhan/socrates-qwen2.5-14b-dpo-mlx-q4"

echo "Step 1: Downloading and converting/quantizing the model to 4-bit MLX..."
echo "This will download 28 GB of raw weights, quantize them, and save the 4-bit quantized version (~8.5 GB)."
echo "Depending on your internet connection, this may take a while."

mlx_lm convert \
  --hf-path socratesft/socrates-qwen2.5-14b-dpo \
  --mlx-path "$MLX_MODEL_PATH" \
  -q

echo "Step 2: Cleaning up Hugging Face cache to free up 28 GB of space..."
rm -rf ~/.cache/huggingface/hub/models--socratesft--socrates-qwen2.5-14b-dpo

echo "Step 3: Creating launcher scripts..."

# Create Chat script
CHAT_SCRIPT="/Users/jaychauhan/socrates-chat.sh"
cat << 'EOF' > "$CHAT_SCRIPT"
#!/bin/bash
echo "Launching Socrates 14B (DPO) Chat CLI..."
source /Users/jaychauhan/mlx_env/bin/activate
mlx_lm.chat --model /Users/jaychauhan/socrates-qwen2.5-14b-dpo-mlx-q4
EOF
chmod +x "$CHAT_SCRIPT"

# Create API Server script
SERVE_SCRIPT="/Users/jaychauhan/socrates-serve.sh"
cat << 'EOF' > "$SERVE_SCRIPT"
#!/bin/bash
echo "Launching Socrates 14B (DPO) OpenAI-Compatible API Server..."
echo "API will be available at http://127.0.0.1:8000/v1"
source /Users/jaychauhan/mlx_env/bin/activate
mlx_lm.server --model /Users/jaychauhan/socrates-qwen2.5-14b-dpo-mlx-q4 --port 8000
EOF
chmod +x "$SERVE_SCRIPT"

echo "=== Setup Completed Successfully ==="
echo "You can now run:"
echo "  - Interactive chat:  ./socrates-chat.sh"
echo "  - Local API server:  ./socrates-serve.sh"
