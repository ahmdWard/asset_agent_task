from fastapi import FastAPI, Depends, HTTPException, status, Query
from app.database import get_db,init_db
from app.routes.crud import asset_crud
from app.config import get_settings
from app.schemas import (
    AssetCreate, AssetResponse, AssetListResponse, AssetUpdate
)
from sqlalchemy.orm import Session



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
    db: Session = Depends(get_db)
):
    """Get all assets"""
    assets = asset_crud.get_all(db, skip=skip, limit=limit)
    total = asset_crud.count(db)
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
    f"{settings.API_V1_PREFIX}/assets/{{asset_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["assets"]
)
def delete_asset(
    asset_id: str,
    db: Session = Depends(get_db)
):
    """Delete an asset (soft delete)"""
    deleted = asset_crud.delete(db, asset_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found"
        )
