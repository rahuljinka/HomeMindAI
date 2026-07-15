import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
from app.routers import auth, rooms, objects, chat, houses

app = FastAPI(title="HomeMind AI API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(houses.router)
app.include_router(rooms.router)
app.include_router(objects.router)
app.include_router(chat.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Welcome to HomeMind AI API"}
