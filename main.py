"""Main entry point for FastAPI server."""
import uvicorn
from app.main import app
from app.core.config import API_HOST, API_PORT

if __name__ == "__main__":
    print(f"\n🚀 Starting Evo-Memory Financial Services API")
    print(f"   Host: {API_HOST}")
    print(f"   Port: {API_PORT}")
    print(f"   API Docs: http://{API_HOST}:{API_PORT}/docs")
    print(f"   Health: http://{API_HOST}:{API_PORT}/api/v1/health\n")
    
    uvicorn.run(app, host=API_HOST, port=API_PORT)

