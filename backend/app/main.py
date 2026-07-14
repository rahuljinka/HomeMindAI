from fastapi import FastAPI
from app.routers import auth, rooms, objects, chat

app = FastAPI(title="HomeMind AI API")

app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(objects.router)
app.include_router(chat.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Welcome to HomeMind AI API"}
