from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import sys
import os
import logging

# Ensure the root directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from crews import crews  # Import the crew definitions
    if not crews:
        raise ValueError("The 'crews' dictionary is empty or not loaded properly!")
except Exception as e:
    logger.error(f"Failed to import 'crews': {e}")
    crews = {}  # Avoid crashes

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development; restrict in production)
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
    # Check if the crew exists
    if request.crew_name not in crews:
        raise HTTPException(status_code=404, detail="Crew not found")

    crew_definition = crews[request.crew_name]

    # Validate required inputs
    missing_keys = [
        key for key in crew_definition.required_inputs.keys() if key not in request.inputs
    ]
    if missing_keys:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required inputs: {', '.join(missing_keys)}",
        )

    # Filter inputs: include only valid required and optional keys
    valid_inputs = {
        k: v for k, v in request.inputs.items()
        if k in crew_definition.required_inputs or k in crew_definition.optional_inputs
    }

    # Execute the selected crew
    output = crew_definition.crew.kickoff(inputs=valid_inputs)

    return {"crew_name": request.crew_name, "output": output}

# Use Railway's assigned PORT dynamically
port = int(os.environ.get("PORT", 8080))

# Run Uvicorn when deployed
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=port)
