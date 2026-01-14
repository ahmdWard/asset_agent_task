from sqlalchemy import Column, String, Float, Date,DateTime
from datetime import datetime
from database import Base
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
    

class AssetStatus:
    ACTIVE = "active"
    SOLD = "sold"
    DONATED = "donated"
    
    @classmethod
    def all(cls):
        return [cls.ACTIVE, cls.SOLD, cls.DONATED]
