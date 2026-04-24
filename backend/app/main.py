from fastapi import FastAPI
from app.api.routes import router
from app.db.database import engine, Base

from fastapi.middleware.cors import CORSMiddleware

# Create tables natively safely
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Waste Routing API")

# Setup Cross-Origin Resource Sharing (CORS) wrapper securely so React can talk
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Since it's local development, allow all incoming origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "healthy", "system": "waste-routing-engine"}
