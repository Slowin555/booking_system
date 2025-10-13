from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

# Import routers (to be created)
# from app.routers import health, users, bookings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up FastAPI application...")
    yield
    # Shutdown
    print("Shutting down FastAPI application...")

app = FastAPI(
    title="Booking API",
    description="A booking system API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://web:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Booking API"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "api"}

# Include routers
# app.include_router(health.router)
# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
