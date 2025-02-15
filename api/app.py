import os
import sys
import logging
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

# Ensure the root directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Safe import of 'crews'
try:
    from crews import crews  
    if not crews:
        raise ValueError("The 'crews' dictionary is empty or not loaded properly!")
except Exception as e:
    logger.error(f"Failed to import 'crews': {e}")
    crews = {}  # Prevents crashes

app = FastAPI()

# Enable CORS (Modify for production security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CrewRequest(BaseModel):
    crew_name: str
    inputs: Dict[str, Any]

@app.get("/")
def root():
    return {"message": "🚀 FastAPI is running on Railway!"}

@app.post("/execute_crew/")
async def execute_crew(request: CrewRequest):
    if request.crew_name not in crews:
        raise HTTPException(status_code=404, detail="Crew not found")

    crew_definition = crews[request.crew_name]

    missing_keys = [
        key for key in crew_definition.required_inputs.keys() if key not in request.inputs
    ]
    if missing_keys:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required inputs: {', '.join(missing_keys)}",
        )

    valid_inputs = {
        k: v for k, v in request.inputs.items()
        if k in crew_definition.required_inputs or k in crew_definition.optional_inputs
    }

    output = crew_definition.crew.kickoff(inputs=valid_inputs)

    return {"crew_name": request.crew_name, "output": output}

# Use Railway's assigned PORT dynamically
port = int(os.environ.get("PORT", 8080))

# ✅ FIX: Run Uvicorn properly without blocking event loop
def run():
    """Start FastAPI server."""
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    asyncio.run(server.serve())

if __name__ == "__main__":
    run()
