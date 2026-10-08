# Lumina AI | ToneShift.ai

Lumina AI is a highly interactive, fast, and modern web application that uses the Gemini API to intelligently rewrite and adjust the tone of emails, messages, and social media posts.

It features a high-production Dark Mode user interface built with HTML/CSS and glassmorphism styling, a backend driven by FastAPI, strict Pydantic input validation, and asynchronous database connections.

## Features

- **A/B Output Comparisons**: Simultaneously generate Assertive and Accommodating versions of your text with a smooth typewriter reveal.
- **Mood Ring**: Live keystroke sentiment analysis that changes the input border color dynamically based on tone (Angry, Calm, Affectionate).
- **Lumina Superpowers**: Specialized rewrite modes, including *Wingman Flirt Optimizer*, *Hype-Man Post Generator*, and *Drunk-Text Translator*.
- **Inbound Analysis**: Toggle Inbound Mode to detect manipulation or gaslighting (Dark Patterns) before you reply.
- **Cinematic Theme Toggle**: Seamless View Transitions API-driven clip-path animations between Dark and Light mode.
- **Accessibility & Security**: Screen-reader ready with ARIA labels, strictly validated endpoints (Pydantic), and locked-down CORS policies for production.

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, Google GenAI SDK, AsyncIOMotorClient (Motor)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5
- **Deployment**: Vercel & Docker

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/AdityaPratapSingh-15/lumina-ai.git
cd lumina-ai
```

### 2. Set up the environment
Create a virtual environment and install the required dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Variables
Copy the example environment file and add your credentials:
```bash
cp .env.example .env
```
Ensure you provide a valid `GEMINI_API_KEY` inside `.env`.

### 4. Run the Development Server
```bash
uvicorn main:app --reload
```
Navigate to [http://localhost:8000](http://localhost:8000) in your browser.

## Testing

The project includes a suite of automated tests. Run them using pytest:
```bash
pytest tests/
```

## Docker Deployment

To run the application inside a Docker container:
```bash
docker build -t lumina-ai .
docker run -p 8080:8080 -e PORT=8080 -e GEMINI_API_KEY="your-api-key" lumina-ai
```
