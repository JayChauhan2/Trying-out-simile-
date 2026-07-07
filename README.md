# Socrates Conjoint LLM Local Runner & Web Dashboard

This repository contains the local runner scripts and a premium web dashboard for the **socrates-qwen2.5-14b-dpo** model. It uses Apple's MLX framework to execute the 14.7B parameter model locally on Apple Silicon at high speeds with a minimal memory footprint.

## 🚀 Key Features

* **4-bit Quantization:** Downsizes the raw 28 GB weights to an optimized 7.8 GB format, running at ~35 tokens/sec with only ~8.4 GB of RAM (perfect for 24 GB Mac laptops).
* **Web Predictor Dashboard:** A gorgeous dark-mode web application featuring:
  * A selector grid of **15 conjoint experiment scenarios** (baseline case, crime severity, gender/race biases, military status, and more).
  * Editable text inputs for **Respondent Demographics**, **Scenario Candidate Attributes**, and **Instruction Constraints**.
  * Visualizer cards that parse candidate attributes on-the-fly.
  * Pulse loader, prediction history, and latency tracking.
* **Interactive CLI Chat:** Fast command-line interface with the model's default system prompt pre-configured.
* **OpenAI-Compatible API:** Exposes a local HTTP server that is compatible with any GPT clients (Chatbox, Page Assist, etc.).

---

## 📂 Project Structure

* [server.py](file:///Users/jaychauhan/socrates_app/server.py) - FastAPI backend that loads the MLX model and exposes the inference API.
* [static/index.html](file:///Users/jaychauhan/socrates_app/static/index.html) - Premium vanilla HTML/CSS/JS single-page frontend.
* [setup_socrates.sh](file:///Users/jaychauhan/socrates_app/setup_socrates.sh) - Automates environment setup, model download, 4-bit conversion, and deletes the 28 GB raw cache to save disk space.
* [socrates-web.sh](file:///Users/jaychauhan/socrates_app/socrates-web.sh) - Launcher script that starts the web app and opens the browser to `http://127.0.0.1:8080`.
* [socrates-chat.sh](file:///Users/jaychauhan/socrates_app/socrates-chat.sh) - Launcher script that starts the interactive terminal chat CLI.
* [socrates-serve.sh](file:///Users/jaychauhan/socrates_app/socrates-serve.sh) - Launcher script for the OpenAI-compatible API server.

---

## 💻 How to Run

### 1. Web Predictor Dashboard (Recommended)
To run the server and open the web dashboard:
```bash
./socrates-web.sh
```
*Access the site at:* `http://127.0.0.1:8080`

### 2. Interactive CLI Chat
To start chatting with the model in the terminal:
```bash
./socrates-chat.sh
```

### 3. Start Local OpenAI API
To run a local backend for third-party clients:
```bash
./socrates-serve.sh
```
*API Base URL:* `http://127.0.0.1:8000/v1`

---

## 📊 Local Performance (Tested on M5 Pro Mac)

* **Prompt Processing:** ~30 tokens/sec
* **Token Generation:** ~35 tokens/sec
* **Peak Memory Usage:** ~8.4 GB RAM
