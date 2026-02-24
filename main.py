from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv  # Line 1: Import the loader

load_dotenv()

app = FastAPI()

# --- CONFIGURATION ---
# Line 3: Pull the key from environment memory instead of hardcoding it
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Google AI library
genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "You are an expert meeting analyst applying the Pareto Principle (80/20 rule). "
    "Extract the critical 20% of information that delivers 90% of the context. "
    "Focus on: Decisions Made, Action Items (with owners), Deadlines, Blockers/Risks. "
    "Format as exactly 5-6 bullet points with bold category labels. Max 6 lines."
)

class TranscriptRequest(BaseModel):
    text: str

@app.get("/")
def health_check():
    """Endpoint to check if the backend is running."""
    return {"status": "Backend is online", "model": "Gemini 1.5 Flash"}
@app.post("/summarize")
async def process_summary(request: TranscriptRequest):
    try:
        # STEP 1: Use the 2026 stable Flash model
        model_id = "gemini-2.5-flash" 
        
        # STEP 2: Initialize
        model = genai.GenerativeModel(model_name=model_id)
        
        # STEP 3: Generate
        response = model.generate_content([SYSTEM_PROMPT, request.text])
        return {"summary": response.text}
        
    except Exception as e:
        # If it fails, let's list what's actually available in your terminal
        print("--- Available Models for your Key ---")
        for m in genai.list_models():
            print(m.name)
        raise HTTPException(status_code=500, detail=f"Model {model_id} failed. Check terminal for list.")