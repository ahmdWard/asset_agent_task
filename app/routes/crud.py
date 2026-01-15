from sqlalchemy.orm import Session
from sqlalchemy import  or_
from typing import List, Optional
from datetime import datetime


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
            category=asset_data.category.value,
            value=asset_data.value,
            purchase_date=asset_data.purchase_date,
            status=asset_data.status.value,
            description=asset_data.description
        )
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset
    


    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str]= None,
        status: Optional[str] = None,
        min_value:Optional[int]= None,
        max_value:Optional[int]= None,
        purchase_date_from:Optional[datetime]=None,
        purchase_date_to:Optional[datetime]=None,
        search:Optional[str]=None,
        sort_by:str="created_at",
        order:str="desc"
        ) -> List[Asset]:
        """Get all assets"""

        query = db.query(Asset).filter(Asset.is_deleted == False)
        
        if category:
         query = query.filter(Asset.category == category) # it's not fuzzy search it needs to be exact match!! 

        if status: 
            query = query.filter(Asset.status == status) # same as category


            #### after finishing task clean this code and wrap it insted of ugly if conditions.
        if min_value:
            query = query.filter(Asset.value >= min_value)

        if max_value: 
            query = query.filter(Asset.value <=max_value)

        if purchase_date_from:
           query = query.filter(Asset.purchase_date >= purchase_date_from)

        if purchase_date_to:
           query = query.filter(Asset.purchase_date <= purchase_date_to)

        if search:
            search_filter= or_(
                Asset.name.ilike(f"%{search}%"),
                Asset.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if order == "asc":
            query = query.order_by(getattr(Asset, sort_by).asc())
        else:
            query = query.order_by(getattr(Asset, sort_by).desc())
        
        

        return query.offset(skip).limit(limit).all()

    
    def count(
        self,
        db: Session,
        category: Optional[str]= None,
        status:Optional[str] = None,
        min_value:Optional[int]= None,
        max_value:Optional[int]= None,
        purchase_date_from:Optional[datetime]=None,
        purchase_date_to:Optional[datetime]=None,
        search: Optional[str] = None,
        ) -> int:
        """Count total assets"""
        query = db.query(Asset).filter(Asset.is_deleted == False)
        if category:
         query = query.filter(Asset.category.ilike(category))

        if status: 
            query = query.filter(Asset.status.ilike(status))

        if min_value:
            query = query.filter(Asset.value >= min_value)

        if max_value: 
            query = query.filter(Asset.value <=max_value)

        if purchase_date_from:
           query = query.filter(Asset.purchase_date >= purchase_date_from)

        if purchase_date_to:
           query = query.filter(Asset.purchase_date <= purchase_date_to)

        if search:
            search_filter = or_(
                Asset.name.ilike(f"%{search}%"),
                Asset.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        

        return query.count()
    

    def get_by_id(self, db: Session, asset_id: str) -> Optional[Asset]:
        """Get an asset by ID"""
        return db.query(Asset).filter(
            Asset.id == asset_id,
            Asset.is_deleted == False
        ).first()
    
    def update(self, db:Session, asset_id:str, asset_data:AssetUpdate) -> Optional[Asset]: 
        """ Update an asset by id """
        db_asset = self.get_by_id(db,asset_id)

        if not db_asset: 
            return None
        updated_data = asset_data.model_dump(exclude_unset=True)

        if 'status' in updated_data and updated_data['status']:
            updated_data['status'] = updated_data['status'].value

        if 'category' in updated_data and updated_data['category']:   #missed updating category after adding Asset Category Class 
           updated_data['category'] = updated_data['category'].value

        for field, value in updated_data.items():
            setattr(db_asset, field, value)
        
        db.commit()
        db.refresh(db_asset)
        return db_asset
    
    def delete(self, db: Session, asset_id: str) -> bool:
        """Delete an asset"""
        db_asset = self.get_by_id(db, asset_id)
        
        if not db_asset:
            return False
        
        db.delete(db_asset)
        db.commit()
        
        return True 
    
    def soft_delete(self, db:Session, asset_id: str) -> bool:
        """ soft Delete  an asset (Keeping it in the database)"""
        db_asset = self.get_by_id(db, asset_id)

        if not db_asset:
            return False
        
        db_asset.is_deleted = True
        db_asset.deleted_at = datetime.utcnow()
        db.commit()

        return True;


    



asset_crud = AssetCRUD()
