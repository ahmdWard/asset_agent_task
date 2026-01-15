from sqlalchemy.orm import Session 
from typing import List, Optional

from app.models import Asset
from app.schemas import (AssetCreate, AssetUpdate)


class AssetCRUD:
    """
    CRUD operations for assets all database operations go through this class
    """
    
    def create(self, db: Session, asset_data: AssetCreate) -> Asset:
        """Create a new asset"""
        db_asset = Asset(
            name=asset_data.name,
            category=asset_data.category,
            value=asset_data.value,
            purchase_date=asset_data.purchase_date,
            status=asset_data.status.value,
            description=asset_data.description
        )
        print(type(db_asset.value))
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset
    


    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Asset]:
        """Get all assets (basic version)"""
        return db.query(Asset).filter(
            Asset.status == "active"
        ).offset(skip).limit(limit).all()
    
    def count(self, db: Session) -> int:
        """Count total assets"""
        return db.query(Asset).filter(Asset.status == "active").count()
    

    def get_by_id(self, db: Session, asset_id: str) -> Optional[Asset]:
        """Get an asset by ID"""
        return db.query(Asset).filter(
            Asset.id == asset_id,
            Asset.status == "active"
        ).first()
    
    def update(self, db:Session, asset_id:str, asset_data:AssetUpdate) -> Optional[Asset]: 
        """ Update an asset by id """
        db_asset = self.get_by_id(db,asset_id)

        if not db_asset: 
            return None
        updated_data = asset_data.model_dump(exclude_unset=True)

        if 'status' in updated_data and updated_data['status']:
            updated_data['status'] = updated_data['status'].value

        for field, value in updated_data.items():
            setattr(db_asset, field, value)
        
        db.commit()
        db.refresh(db_asset)
        return db_asset
    
    def delete(self, db: Session, asset_id: str) -> bool:
        """Delete an asset (soft delete by default)"""
        db_asset = self.get_by_id(db, asset_id)
        
        if not db_asset:
            return False
        
        db.delete(db_asset)
        db.commit()
        
        return True    


asset_crud = AssetCRUD()
