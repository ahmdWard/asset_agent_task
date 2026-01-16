from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional
from enum import Enum

from app.models import ( AssetStatus, AssetCategory )




class AssetStatusEnum(str, Enum):
    active = AssetStatus.ACTIVE
    sold = AssetStatus.SOLD
    donated = AssetStatus.DONATED


class AssetCategoryEnum(str, Enum):
    electronics = AssetCategory.ELECTRONICS
    furniture = AssetCategory.FURNITURE
    vehicle = AssetCategory.VEHICLE
    jewelry = AssetCategory.JEWELRY
    other = AssetCategory.OTHER



class AssetBase(BaseModel):
    """Base asset schema with common fields"""
    name: str = Field(..., min_length=1, max_length=200, description="Asset name")
    category:AssetCategoryEnum = Field(..., description="Asset category")
    value: float = Field(..., gt=0, description="Asset value (must be positive)")
    purchase_date: date = Field(..., description="Purchase date (YYYY-MM-DD)")
    status: AssetStatusEnum = Field(default=AssetStatusEnum.active, description="Asset status")
    description: Optional[str] = Field(None, max_length=500, description="Optional description")

    # #### fixing adding purches_date in the future 
    # @field_validator('purchase_date')
    # def validate_purchase_date(cls, purchase_date):
    #     if purchase_date > date.today():
    #         raise ValueError('purchase_date cannot be in the future')
    #     return purchase_date


class AssetCreate(AssetBase):
    """Schema for creating a new asset (what user sends in POST request)"""
    pass

class AssetResponse(AssetBase):
    """Schema for asset response (what API returns)"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 

class AssetListResponse(BaseModel):
    """Schema for paginated list of assets"""
    total: int
    assets: list[AssetResponse]



class AssetUpdate(BaseModel):
    """Schema for updating new asset"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[AssetCategoryEnum] = None
    value: Optional[float] = Field(None, gt=0)
    purchase_date: Optional[date] = None
    status: Optional[AssetStatusEnum] = None
    description: Optional[str] = Field(None, max_length=500)



class AgentQuery(BaseModel):
    question: str = Field(..., min_length=1, description="Question about assets")


class AgentResponse(BaseModel):
    answer: str
    sources: list[str] = []
    query_type: str = "general"
    assets_found: Optional[int] = None