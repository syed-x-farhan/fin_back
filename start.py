#!/usr/bin/env python3
"""
Startup script for the Financial Modeling API
"""

import os
import uvicorn
from main import app

if __name__ == "__main__":
    # Get port from environment variable (Railway provides this)
    port = int(os.environ.get("PORT", 8000))
    
    print("🚀 Starting Financial Modeling API...")
    print(f"📊 Backend will be available at: http://0.0.0.0:{port}")
    print(f"📚 API Documentation at: http://0.0.0.0:{port}/docs")
    print(f"🔧 Health check at: http://0.0.0.0:{port}/health")
    print("=" * 50)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )
