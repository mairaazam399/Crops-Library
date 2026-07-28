from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .schemas import IdentifyResponse, SpeciesPrediction
from typing import List
import io
from PIL import Image

app = FastAPI(title="Crops Library - Backend (stub)")

# Allow requests from the mobile app (you can lock this down in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/identify", response_model=IdentifyResponse)
async def identify(file: UploadFile = File(...)):
    """Accept an image upload and return a stubbed plant identification result.

    Replace the stub logic with a real ML model inference later.
    """
    contents = await file.read()
    # quick validation: ensure we got an image
    try:
        img = Image.open(io.BytesIO(contents))
        img.verify()
    except Exception:
        return IdentifyResponse(
            success=False,
            error="Uploaded file is not a valid image",
            predictions=[],
        )

    # Stubbed deterministic response based on file size to make quick testing repeatable
    size = len(contents)
    if size % 3 == 0:
        predictions = [
            SpeciesPrediction(name="Zea mays (Maize)", confidence=0.87),
            SpeciesPrediction(name="Sorghum bicolor", confidence=0.08),
        ]
    else:
        predictions = [
            SpeciesPrediction(name="Solanum lycopersicum (Tomato)", confidence=0.72),
            SpeciesPrediction(name="Capsicum annuum (Pepper)", confidence=0.13),
        ]

    return IdentifyResponse(success=True, error=None, predictions=predictions)


@app.post("/diagnose", response_model=IdentifyResponse)
async def diagnose(file: UploadFile = File(...)):
    """Stubbed disease diagnosis endpoint. Returns placeholder disease labels."""
    contents = await file.read()
    # naive stub: return 'healthy' or 'blight' based on parity of bytes
    if len(contents) % 2 == 0:
        predictions = [SpeciesPrediction(name="Healthy", confidence=0.92)]
    else:
        predictions = [SpeciesPrediction(name="Late blight", confidence=0.78)]

    return IdentifyResponse(success=True, error=None, predictions=predictions)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
