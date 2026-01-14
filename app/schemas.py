from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional
from enum import Enum

from app.models import AssetStatus




class AssetStatusEnum(str, Enum):
    active = AssetStatus.ACTIVE
    sold = AssetStatus.SOLD
    donated = AssetStatus.DONATED



class AssetBase(BaseModel):
    """Base asset schema with common fields"""
    name: str = Field(..., min_length=1, max_length=200, description="Asset name")
    category:str = Field(..., description="Asset category")
    value: float = Field(..., gt=0, description="Asset value (must be positive)")
    purchase_date: date = Field(..., description="Purchase date (YYYY-MM-DD)")
    status: AssetStatusEnum = Field(default=AssetStatusEnum.active, description="Asset status")
    description: Optional[str] = Field(None, max_length=500, description="Optional description")


