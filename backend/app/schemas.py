from pydantic import BaseModel
from typing import Optional, List


class SpeciesPrediction(BaseModel):
    name: str
    confidence: float


class IdentifyResponse(BaseModel):
    success: bool
    error: Optional[str]
    predictions: List[SpeciesPrediction]
