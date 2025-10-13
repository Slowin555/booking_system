#!/usr/bin/env python3
"""
Simple test script to verify FastAPI setup
"""

try:
    from fastapi import FastAPI
    print("✅ FastAPI imported successfully")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")

try:
    import uvicorn
    print("✅ Uvicorn imported successfully")
except ImportError as e:
    print(f"❌ Uvicorn import failed: {e}")

# Test basic FastAPI app
try:
    app = FastAPI(title="Test API")
    
    @app.get("/")
    def read_root():
        return {"message": "Hello World"}
    
    @app.get("/health")
    def health_check():
        return {"status": "ok", "service": "api"}
    
    print("✅ FastAPI app created successfully")
    print("✅ Health endpoint configured")
    
    # Test if we can run the server
    print("🚀 Starting test server on http://localhost:8000")
    print("📋 Available endpoints:")
    print("   - GET /")
    print("   - GET /health")
    print("   - GET /docs (FastAPI docs)")
    print("\n⏹️  Press Ctrl+C to stop the server")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    
except Exception as e:
    print(f"❌ Error creating FastAPI app: {e}")
