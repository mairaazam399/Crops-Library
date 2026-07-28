from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Crop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    common_name: str
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CropCreate(SQLModel):
    common_name: str
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    description: Optional[str] = None


class CropRead(Crop):
    pass


class CropUpdate(SQLModel):
    common_name: Optional[str] = None
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    description: Optional[str] = None
