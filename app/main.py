from fastapi import FastAPI, Depends, HTTPException, status, Query
from app.database import get_db,init_db
from app.routes.crud import asset_crud
from app.config import get_settings
from app.schemas import (
    AssetCreate, AssetResponse, AssetListResponse, AssetUpdate
)
from sqlalchemy.orm import Session

from typing import Optional
from datetime import datetime




settings = get_settings()


app = FastAPI(
    title=settings.PROJECT_NAME,
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print(f" {settings.PROJECT_NAME} started!")


@app.get("/")
async def root():
    return {"message": "test_test"}



@app.post(
    f"{settings.API_V1_PREFIX}/assets",
    response_model=AssetResponse,
    status_code=status.HTTP_201_CREATED
)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db)
):
    try:
        db_asset = asset_crud.create(db, asset)
        return db_asset
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    f"{settings.API_V1_PREFIX}/assets",
    response_model=AssetListResponse,
    tags=["assets"]
)
def get_assets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    min_value:Optional[int] =Query(None,description="Filter by Min value"),
    max_value:Optional[int]=Query(None,description="Filter by Max Value"),
    purchase_date_from:Optional[datetime]= Query(None,description="Filter by purchase_date_from"),
    purchase_date_to:Optional[datetime]= Query(None,description="Filter by purchase_date_to"),
    search:Optional[str]=Query(None,description="Filter using search keyWord"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),

):
    """Get all assets"""
    assets = asset_crud.get_all(db, skip, limit, category, status, min_value, max_value,purchase_date_from,purchase_date_to,search,sort_by,order)
    total = asset_crud.count(db, category, status,min_value, max_value,purchase_date_from,purchase_date_to,search)
    return AssetListResponse(total=total, assets=assets)


@app.get(
    f"{settings.API_V1_PREFIX}/assets/{{asset_id}}",
    response_model=AssetResponse,
    tags=["assets"]
)
def get_asset(
    asset_id: str,
    db: Session = Depends(get_db)
):
    """Get asset by ID"""
    asset = asset_crud.get_by_id(db, asset_id)
    
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found"
        )
    
    return asset



@app.put(
    f"{settings.API_V1_PREFIX}/assets/{{asset_id}}",
    response_model=AssetResponse,
    tags=["assets"]
)
def update_asset(
    asset_id: str,
    asset: AssetUpdate,
    db: Session = Depends(get_db)
):
    """Update an asset"""
    db_asset = asset_crud.update(db, asset_id, asset)
    
    if not db_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found"
        )
    
    return db_asset


@app.delete(
    f"{settings.API_V1_PREFIX}/assets/{{asset_id}}/hard-delete",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["assets"]
)
def delete_asset(
    asset_id: str,
    db: Session = Depends(get_db)
):
    """Delete an asset (Hard delete)"""
    deleted = asset_crud.delete(db, asset_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found"
        )
    

@app.delete(
    f"{settings.API_V1_PREFIX}/assets/{{asset_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["assets"]
)
def delete_asset(
    asset_id: str,
    db: Session = Depends(get_db)
):
    """Delete an asset (soft delete)"""
    deleted = asset_crud.soft_delete(db, asset_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found"
        )