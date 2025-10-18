from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
"Просто текст ради теста фетча"
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

# Routers
from app.auth.register import router as register_router  # noqa: E402
from app.auth.login import router as login_router  # noqa: E402
from app.auth.logout import router as logout_router  # noqa: E402
from app.auth.me import router as me_router  # noqa: E402
from app.auth.refresh import router as refresh_router  # noqa: E402
from app.auth.ratelimit import limiter  # noqa: E402
from slowapi.errors import RateLimitExceeded  # noqa: E402
from slowapi.middleware import SlowAPIMiddleware  # noqa: E402

app.include_router(register_router)
app.include_router(login_router)
app.include_router(logout_router)
app.include_router(me_router)
app.include_router(refresh_router)

# Rate limiting
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request, exc):
    return await limiter._rate_limit_exceeded_handler(request, exc)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
