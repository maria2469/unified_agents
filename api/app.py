from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import sys
import os

# Ensure the root directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crews import crews  # Import the crew definitions

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; modify this for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CrewRequest(BaseModel):
    crew_name: str
    inputs: Dict[str, Any]

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

# Start the server only for local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
