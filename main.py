import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

app = FastAPI(title="Email Rewriter API")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Gemini client (expects GEMINI_API_KEY environment variable)
try:
    client = genai.Client()
except Exception as e:
    client = None
    print(f"Failed to initialize GenAI client: {e}")

MONGO_URI = os.environ.get("MONGO_URI")
try:
    if MONGO_URI:
        mongo_client = AsyncIOMotorClient(MONGO_URI)
        db = mongo_client.get_database("lumina_ai")
    else:
        mongo_client = None
        db = None
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

class RewriteRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=2000)
    relationship_context: str = "University Professor"
    tone: str = "Professional & Polite"
    cultural_norm: str = "Global Neutral"
    specialized_mode: str = "Standard"
    is_inbound: bool = False

class RewriteResponse(BaseModel):
    assertive_version: str
    accommodating_version: str
    dark_pattern_warning: Optional[str] = None

class ReactRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=2000)

class ReactResponse(BaseModel):
    reaction: str

class SentimentResponse(BaseModel):
    sentiment: str

@app.post("/sentiment", response_model=SentimentResponse)
def get_sentiment(req: ReactRequest):
    if not client:
        raise HTTPException(status_code=500, detail="Gemini client is not initialized.")
    try:
        sys_inst = "Analyze the text and return EXACTLY ONE of these three words based on its dominant emotion: 'angry', 'calm', or 'affectionate'."
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=req.text,
            config={"system_instruction": sys_inst}
        )
        sentiment = response.text.strip().lower()
        if "angry" in sentiment: sentiment = "angry"
        elif "affectionate" in sentiment: sentiment = "affectionate"
        else: sentiment = "calm"
        return SentimentResponse(sentiment=sentiment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/react", response_model=ReactResponse)
def react_to_text(req: ReactRequest):
    if not client:
        raise HTTPException(status_code=500, detail="Gemini client is not initialized.")
    
    try:
        system_instruction = "You are a highly empathetic, casual best friend. Analyze the emotional undertone of the text. If the text reveals stress, sadness, frustration, or anxiety, respond with casual, genuine consolation (e.g., 'Whoa, this sounds heavy. Are you holding up okay?'). Keep the reaction to 1-2 short, conversational sentences. If there is no negative emotion, return the exact string 'NONE'."
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=req.text,
            config={"system_instruction": system_instruction}
        )
        return ReactResponse(reaction=response.text.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rewrite", response_model=RewriteResponse)
def rewrite_email(req: RewriteRequest):
    if not client:
        raise HTTPException(status_code=500, detail="Gemini client is not initialized. Please ensure GEMINI_API_KEY is set.")
    
    try:
        # Build mode instructions
        mode_rules = ""
        if req.specialized_mode == "Wingman Flirt Optimizer":
            mode_rules = "Mode: Wingman. Make it funny and engaging. CRITICAL GUARDRAIL: Flag and rewrite anything that sounds creepy or aggressive into something charming and respectful."
        elif req.specialized_mode == "Hype-Man Post Generator":
            mode_rules = "Mode: Hype-Man. Rewrite modest achievements into viral, engaging social media formats."
        elif req.specialized_mode == "Hinglish Processor":
            mode_rules = "Mode: Hinglish. Maintain the exact cultural blend of Hindi and English instead of standardizing to plain English."
        elif req.specialized_mode == "Regional Slang Localizer" or req.specialized_mode == "Colloquial Idiom Matcher":
            mode_rules = "Mode: Slang/Idioms. Keep and enhance the specific regional slang, idioms, or Gen-Z expressions."
        elif req.specialized_mode == "Drunk-Text Translator":
            mode_rules = "Mode: Drunk-Text. Fix heavy typos and infer the actual intended meaning into a coherent message."
        elif req.specialized_mode == "Voice-Cadence Mimic":
            mode_rules = "Mode: Voice-Cadence Mimic. Preserve the user's natural spacing, ellipses, and filler words (like 'umm', 'like') while fixing the underlying tone."
            
        inbound_rules = ""
        if req.is_inbound:
            inbound_rules = "The input text is an INBOUND received message. Analyze it for dark patterns, gaslighting, false urgency, or guilt-tripping. If detected, output a short warning in 'dark_pattern_warning', otherwise set it to null. Then, draft a firm, boundary-setting reply."

        system_instruction = f"You are an expert copywriter and analyst. {inbound_rules}\nRewrite the following text for a '{req.relationship_context}'. Maintain a '{req.tone}' tone, and rigidly apply '{req.cultural_norm}' cultural etiquette. {mode_rules}\nReturn a strict JSON object with 'assertive_version', 'accommodating_version', and 'dark_pattern_warning'."
        
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=req.text,
            config={
                "system_instruction": system_instruction,
                "response_mime_type": "application/json",
                "response_schema": RewriteResponse,
            }
        )
        
        # Parse the JSON response
        result = json.loads(response.text)
        return RewriteResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="Frontend HTML not found.")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()
