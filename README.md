# Email Rewriter Backend

This is a lightweight Python FastAPI backend that takes user text, sends it to the Gemini API (using the new `client.interactions.create` endpoint) with a system prompt to rewrite emails, and returns the response.

## Setup

1. The dependencies have already been installed in a virtual environment (`.venv`).
2. You will need a Gemini API key. Set it as an environment variable before running the application.

```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Running the Server

Start the FastAPI application using `uvicorn`:

```bash
source .venv/bin/activate
uvicorn main:app --reload
```

The server will be running at `http://127.0.0.1:8000`.

## Testing the Endpoints

### 1. Health Check
```bash
curl http://127.0.0.1:8000/
```
**Expected Response:**
```json
{"status":"ok","message":"Email Rewriter API is running"}
```

### 2. Rewrite Email
```bash
curl -X POST "http://127.0.0.1:8000/rewrite" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hey there, just following up on that thing."}'
```
**Expected Response:**
```json
{"rewritten_text":"..."}
```
