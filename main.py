import os
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
if not GOOGLE_GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

# Get system prompt from file (path provided in .env)
SYSTEM_PROMPT_PATH = os.getenv("SYSTEM_PROMPT_PATH", "system_prompt.txt")
try:
    RUMENYI_SYSTEM_MESSAGE = Path(SYSTEM_PROMPT_PATH).read_text()
    #print(RUMENYI_SYSTEM_MESSAGE)
except Exception as e:
    raise RuntimeError(f"Failed to read system prompt file at {SYSTEM_PROMPT_PATH}: {e}")

# Set up FastAPI app
app = FastAPI()

# Allow CORS (update origin if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEFAULT_MODEL_NAME = "gemini-2.5-flash"

async def get_gemini_response(
    user_message: str,
    chat_history: list = None,
    model_name: str = DEFAULT_MODEL_NAME,
) -> str:
    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=RUMENYI_SYSTEM_MESSAGE
        )

        chat = model.start_chat(history=chat_history if chat_history else [])

        response_stream = await chat.send_message_async(user_message, stream=True)

        full_response_text = ""
        async for chunk in response_stream:
            if chunk.text:
                full_response_text += chunk.text

        if not full_response_text:
            print(f"Warning: Gemini API returned an empty response for: '{user_message}'")
            return "Désolé, je n'ai pas pu générer de réponse pour le moment. Veuillez réessayer."

        return full_response_text

    except Exception as e:
        error_message = f"Erreur lors de la communication avec l'API Gemini : {e}"
        print(error_message)
        raise Exception(error_message)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    user_message = data.get("message")
    chat_history = data.get("history", None)
    model_name = data.get("model_name", DEFAULT_MODEL_NAME)

    if not user_message:
        raise HTTPException(status_code=400, detail="Field 'message' is required")

    try:
        response_text = await get_gemini_response(
            user_message=user_message,
            chat_history=chat_history,
            model_name=model_name,
        )
        return {"response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
