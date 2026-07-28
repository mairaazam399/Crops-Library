from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import IdentifyResponse, SpeciesPrediction
from .models import Crop, CropCreate, CropRead, CropUpdate
from .db import init_db, get_session
from typing import List, Optional
import io
from PIL import Image
from sqlmodel import select
import os

# AI helpers
from . import ai_openai

app = FastAPI(title="Crops Library - Backend (OpenAI)")

# Allow requests from the mobile/web app (you can lock this down in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Initialize DB and seed some sample crops if empty
    init_db()
    with get_session() as session:
        statement = select(Crop)
        results = session.exec(statement)
        any_crop = results.first()
        if not any_crop:
            samples = [
                Crop(common_name="Maize", scientific_name="Zea mays", family="Poaceae", description="Important cereal crop."),
                Crop(common_name="Tomato", scientific_name="Solanum lycopersicum", family="Solanaceae", description="Widely cultivated edible fruit."),
                Crop(common_name="Wheat", scientific_name="Triticum aestivum", family="Poaceae", description="Staple cereal worldwide."),
            ]
            for c in samples:
                session.add(c)
            session.commit()


@app.post("/identify", response_model=IdentifyResponse)
async def identify(file: UploadFile = File(...)):
    """Accept an image upload and return either a real AI identification (if OPENAI_API_KEY is set)
    or a deterministic stubbed response for development.
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

    # If OpenAI is configured, call it
    if os.getenv('OPENAI_API_KEY'):
        try:
            # ai_openai.identify_image_bytes is async
            parsed = await ai_openai.identify_image_bytes(contents)
            preds = parsed.get('predictions', [])
            predictions = []
            for p in preds:
                name = p.get('name')
                typ = p.get('type', 'species')
                conf = float(p.get('confidence', 0))
                predictions.append(SpeciesPrediction(name=f"{name} ({typ})", confidence=conf))

            return IdentifyResponse(success=True, error=None, predictions=predictions)
        except Exception as e:
            # If the AI call fails, return a useful error and fall back to stubbed response
            error_msg = f"AI inference failed: {str(e)}"
            # produce stubbed response so the app remains functional
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

            return IdentifyResponse(success=False, error=error_msg, predictions=predictions)

    # Fallback: deterministic stub (no AI key set)
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


# --- Crops CRUD endpoints ---

@app.post("/crops", response_model=CropRead)
def create_crop(payload: CropCreate):
    with get_session() as session:
        crop = Crop.from_orm(payload)
        session.add(crop)
        session.commit()
        session.refresh(crop)
        return crop


@app.get("/crops", response_model=List[CropRead])
def list_crops(limit: Optional[int] = 100):
    with get_session() as session:
        statement = select(Crop).limit(limit)
        results = session.exec(statement).all()
        return results


@app.get("/crops/{crop_id}", response_model=CropRead)
def get_crop(crop_id: int):
    with get_session() as session:
        crop = session.get(Crop, crop_id)
        if not crop:
            raise HTTPException(status_code=404, detail="Crop not found")
        return crop


@app.put("/crops/{crop_id}", response_model=CropRead)
def update_crop(crop_id: int, payload: CropUpdate):
    with get_session() as session:
        crop = session.get(Crop, crop_id)
        if not crop:
            raise HTTPException(status_code=404, detail="Crop not found")
        crop_data = payload.dict(exclude_unset=True)
        for key, val in crop_data.items():
            setattr(crop, key, val)
        session.add(crop)
        session.commit()
        session.refresh(crop)
        return crop


@app.delete("/crops/{crop_id}")
def delete_crop(crop_id: int):
    with get_session() as session:
        crop = session.get(Crop, crop_id)
        if not crop:
            raise HTTPException(status_code=404, detail="Crop not found")
        session.delete(crop)
        session.commit()
        return {"success": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
