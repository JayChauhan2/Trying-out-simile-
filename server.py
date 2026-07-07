import os
import json
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from mlx_lm import load, generate

app = FastAPI(title="Socrates Local Web App")

# Paths
MODEL_PATH = "/Users/jaychauhan/socrates-qwen2.5-14b-dpo-mlx-q4"
FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "feedback.json")

print("Loading MLX model...")
start_time = time.time()
model, tokenizer = load(MODEL_PATH)
print(f"Model loaded in {time.time() - start_time:.2f} seconds.")

class PredictionRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    max_tokens: int = 50

class FeedbackRequest(BaseModel):
    scenario_index: int
    status: str  # "correct", "incorrect", or ""

@app.post("/api/predict")
async def predict(req: PredictionRequest):
    try:
        messages = [
            {"role": "system", "content": req.system_prompt},
            {"role": "user", "content": req.user_prompt}
        ]
        
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        
        start_inference = time.time()
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

@app.get("/api/feedback")
async def get_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return {}
    try:
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        return {}

@app.post("/api/feedback")
async def save_feedback(req: FeedbackRequest):
    data = {}
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            data = {}
            
    data[str(req.scenario_index)] = req.status
    
    try:
        with open(FEEDBACK_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return {"status": "success"}
    except Exception as e:
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
