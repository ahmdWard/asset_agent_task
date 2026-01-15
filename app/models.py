from sqlalchemy import Column, String, Float, Date, DateTime, Boolean
from datetime import datetime
from app.database import Base
import uuid


def generate_uuid():
    """Generate UUID string for asset ID"""
    return str(uuid.uuid4())

class Asset(Base):
    __tablename__ = "assets"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    name = Column(String,nullable=False, index=True)
    category = Column(String,nullable=False)
    value = Column(Float,nullable=False)
    purchase_date = Column(Date,nullable=False)
    status = Column(String,nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    description = Column(String(500), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime, nullable=True)

    

class AssetStatus:
    ACTIVE = "active"
    SOLD = "sold"
    DONATED = "donated"
    
    @classmethod
    def all(cls):
        return [cls.ACTIVE, cls.SOLD, cls.DONATED]
    

class AssetCategory:
    """Valid asset category values"""
    ELECTRONICS = "electronics"
    FURNITURE = "furniture"
    VEHICLE = "vehicle"
    JEWELRY = "jewelry"
    OTHER = "other"
    
    @classmethod
    def all(cls):
        return [cls.ELECTRONICS, cls.FURNITURE, cls.VEHICLE, cls.JEWELRY, cls.OTHER]
    

