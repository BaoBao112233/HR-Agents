from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
import os
from pathlib import Path

from jd_assistants.clickhouse_db import init_clickhouse, get_user_by_email, get_user_by_id, create_user
from jd_assistants.auth import (
    create_user_token, verify_token,
    Token, UserRegister, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
)

# User roles
class UserRole:
    ADMIN = "admin"
    MANAGER = "manager"
    HR = "hr"
    USER = "user"

# Create FastAPI app
app = FastAPI(
    title="HR Management System",
    description="Comprehensive HRMS with AI-powered recruitment",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Vite dev server
        "http://localhost:5173",  # Alternative Vite port
        "http://localhost:8000",  # Production (same origin)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception
    
    user = get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_clickhouse()
    print("✅ ClickHouse database initialized")

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "2.0.0"}

# ===== AUTH ENDPOINTS =====
@app.post("/api/v1/auth/register", response_model=Token)
async def register(user_data: UserRegister):
    """Register a new user"""
    # Check if user exists
    existing_user = get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create user
    password_hash = get_password_hash(user_data.password)
    user_dict = {
        "email": user_data.email,
        "password_hash": password_hash,
        "role": user_data.role
    }
    user = create_user(user_dict)
    
    # Create token
    access_token = create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/v1/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    # Get user by email
    user = get_user_by_email(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
@app.get("/api/v1/auth/me")
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

# ===== DASHBOARD =====
@app.get("/api/v1/dashboard")
async def get_dashboard(current_user = Depends(get_current_user)):
    """Get dashboard data"""
    # TODO: Implement dashboard logic
    return {
        "message": "Dashboard endpoint",
        "user": current_user.email,
        "role": current_user.role
    }

# ===== INCLUDE ROUTERS =====
# ===== INCLUDE ROUTERS =====
from jd_assistants.backend.api.v1.recruitment_v2 import router as recruitment_router
from jd_assistants.backend.api.v1.api_keys import router as api_keys_router

app.include_router(recruitment_router)
app.include_router(api_keys_router)
# ===== STATIC FILES =====
# Mount static files for production
static_dir = Path("/app/static")
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets")
    
    # Serve index.html for all non-API routes (SPA fallback)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Don't intercept API routes
        if full_path.startswith("api/") or full_path.startswith("health"):
            raise HTTPException(status_code=404, detail="Not found")
        
        # Serve index.html for all other routes
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        raise HTTPException(status_code=404, detail="Frontend not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

