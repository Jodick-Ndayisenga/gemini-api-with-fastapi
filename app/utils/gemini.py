import google.generativeai as genai
# load dotenv
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

# --- Configuration ---
# Your Gemini API Key from settings.
# A ValueError is raised early if the key isn't found, ensuring critical dependency.

if not GOOGLE_GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in configuration settings. Please ensure it's defined in config.py.")

genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

# Default model name for consistency.
# Using 'gemini-1.5-flash' as it's the most common "flash" model identifier.
# If you specifically intended another version like 'gemini-1.5-pro', adjust this.
DEFAULT_MODEL_NAME = "gemini-2.5-flash"

# --- System Message for Rumenyi Chatbot ---
# This message defines the AI's persona and core purpose.
RUMENYI_SYSTEM_MESSAGE = """
You are Rumenyi, a multilingual digital agricultural assistant dedicated to empowering small-scale farmers in Burundi.
Your primary goal is to provide timely, accurate, and personalized agronomic advice to help farmers improve crop care,
predict and manage plant diseases (especially potato late blight), diagnose soil types, and match crops to appropriate soils.
Communicate clearly and encouragingly in local languages (Kirundi, French, Swahili, or English, as appropriate),
bridging information gaps and addressing challenges like climate variability, pests, and limited access to modern farming techniques.
Focus on practical, actionable advice to enhance productivity, increase yields, and foster food security and economic resilience for Burundian farming families.
"""

# --- Gemini API Interaction Function ---
async def get_gemini_response(
    user_message: str,
    chat_history: list = None, # Renamed for clarity, None is default for new chats
    model_name: str = DEFAULT_MODEL_NAME,
) -> str:
    """
    Interacts with the Google Gemini API to get a response for a chatbot.

    Args:
        user_message (str): The new message from the user.
        chat_history (list, optional): A list of previous chat messages. Each element
                                      should be a dictionary like:
                                      {"role": "user", "parts": [{"text": "..."}]} or
                                      {"role": "model", "parts": [{"text": "..."}]}.
                                      Defaults to None, starting a new chat session.
        model_name (str, optional): The Gemini model to use (e.g., "gemini-1.5-flash").
                                    Defaults to DEFAULT_MODEL_NAME.

    Returns:
        str: The generated text response from the Gemini model.

    Raises:
        Exception: If there's an error communicating with the Gemini API.
    """
    try:
        # Initialize the GenerativeModel with the specified model and system instruction.
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=RUMENYI_SYSTEM_MESSAGE
        )

        # Start a chat session. If chat_history is provided, it's loaded.
        # Otherwise, a new session begins.
        chat = model.start_chat(history=chat_history if chat_history is not None else [])

        # Send the user's message asynchronously and stream the response for efficiency.
        response_stream = await chat.send_message_async(user_message, stream=True)

        full_response_text = ""
        # Iterate over chunks to build the complete response.
        async for chunk in response_stream:
            # Ensure chunk.text is not None before appending
            if chunk.text:
                full_response_text += chunk.text

        # If after streaming, the response is still empty, it might indicate an issue
        if not full_response_text:
            print(f"Warning: Gemini API returned an empty response for message: '{user_message}'")
            # You might want to raise a specific error here or return a default message
            return "Désolé, je n'ai pas pu générer de réponse pour le moment. Veuillez réessayer."

        return full_response_text

    except Exception as e:
        # Catch any exceptions during the API call and re-raise them after logging.
        # This allows the calling function (e.g., your API endpoint) to handle it.
        error_message = f"Erreur lors de la communication avec l'API Gemini : {e}"
        print(error_message) # Log the error
        raise Exception(error_message) # Re-raise for upstream handling