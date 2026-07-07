import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from mlx_lm import load, generate

app = FastAPI(title="Socrates Local Web App")

# Model path
MODEL_PATH = "/Users/jaychauhan/socrates-qwen2.5-14b-dpo-mlx-q4"

print("Loading MLX model...")
start_time = time.time()
model, tokenizer = load(MODEL_PATH)
print(f"Model loaded in {time.time() - start_time:.2f} seconds.")

class PredictionRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    max_tokens: int = 50

@app.post("/api/predict")
async def predict(req: PredictionRequest):
    try:
        messages = [
            {"role": "system", "content": req.system_prompt},
            {"role": "user", "content": req.user_prompt}
        ]
        
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        
        start_inference = time.time()
        # MLX generate returns the text
        response = generate(model, tokenizer, prompt=prompt, max_tokens=req.max_tokens)
        duration = time.time() - start_inference
        
        clean_response = response.strip()
        
        return {
            "prediction": clean_response,
            "latency_seconds": duration,
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Serve the static index.html
@app.get("/")
async def get_index():
    static_file = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    else:
        return HTMLResponse(content="<h1>Frontend index.html not found!</h1>", status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
