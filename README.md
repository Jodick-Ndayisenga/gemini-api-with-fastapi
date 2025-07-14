# Rufuku - Agricultural AI Assistant

## Overview
Rumenyi is a multilingual digital agricultural assistant powered by Google's Gemini AI, designed specifically for small-scale farmers in Burundi. The assistant provides personalized agronomic advice, disease management guidance, and soil analysis support in multiple languages including Kirundi, French, Swahili, and English.

## Features
- 🌱 Personalized agronomic advice
- 🦠 Plant disease prediction and management (especially potato late blight)
- 🌍 Soil type diagnosis and crop matching
- 🗣️ Multilingual support (Kirundi, French, Swahili, English)
- 💬 Real-time chat interface
- 🔄 Streaming responses for better user experience

## Tech Stack

- FastAPI for backend API
- Google Gemini AI for intelligent responses
- Docker for containerization
- Python 3.11.5
- Uvicorn ASGI server

## Prerequisites
- Python 3.11.5
- Docker and Docker Compose
- Google Gemini API key

## Installation

### Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/Jodick-Ndayisenga/gemini-api-with-fastapi.git
   cd gardien-vert/genai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file with your Google Gemini API key:
   ```env
   GOOGLE_GEMINI_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Deployment
1. Build and start the container:
   ```bash
   docker-compose up --build
   ```

## API Endpoints

### GET /
- Health check endpoint
- Returns: `{"message": "Hello, World!"}`

### POST /chat
- Main chat endpoint for interacting with Rumenyi
- Request body:
  ```json
  {
    "message": "string",
    "history": [optional chat history],
    "model_name": "string (optional)"
  }
  ```
- Response:
  ```json
  {
    "response": "string"
  }
  ```

## Environment Variables
- `GOOGLE_GEMINI_API_KEY`: Your Google Gemini API key (required)
- `SYSTEM_PROMPT`: Your system prompt for the Gemini AI model (required)

## Development

### Project Structure
```
├── app/
│   └── utils/
│       └── gemini.py    # Gemini AI integration
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── docker-compose.yml  # Container orchestration
└── .env                # Environment variables
```

### Adding New Features
1. Create new endpoints in `main.py`
2. Add utility functions in `app/utils/`
3. Update requirements.txt if new dependencies are added
4. Document changes in this README

## Testing
To run tests (when implemented):
```bash
python -m pytest
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Add your license here]

## Contact
[Add your contact information]