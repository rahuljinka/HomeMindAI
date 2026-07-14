from fastapi import FastAPI
from backend.app.routers import auth

app = FastAPI(title="HomeMind AI API")

app.include_router(auth.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Welcome to HomeMind AI API"}
