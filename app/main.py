from fastapi import FastAPI
import app.models as models ,app.database as database
from app.routes import assets

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(assets.router)

@app.get("/")
async def root():
    return {"message": "test_test"}