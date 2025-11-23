from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
import os

from jd_assistants.database import get_session, init_db
from jd_assistants.auth import (
    authenticate_user, create_user_token, verify_token,
    Token, UserRegister, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
)
from jd_assistants.database import create_user, UserRole

# Create FastAPI app
app = FastAPI(
    title="HR Management System",
    description="Comprehensive HRMS with AI-powered recruitment",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Dependency to get current user
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception
    
    from jd_assistants.database import get_user_by_email
    user = await get_user_by_email(session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()
    print("✅ Database initialized")

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "2.0.0"}

# ===== AUTH ENDPOINTS =====
@app.post("/api/v1/auth/register", response_model=Token)
async def register(
    user_data: UserRegister,
    session: AsyncSession = Depends(get_session)
):
    """Register a new user"""
    # Check if user exists
    from jd_assistants.database import get_user_by_email
    existing_user = await get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create user
    password_hash = get_password_hash(user_data.password)
    user = await create_user(
        session,
        email=user_data.email,
        password_hash=password_hash,
        role=UserRole(user_data.role)
    )
    
    # Create token
    access_token = create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/v1/auth/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Login and get access token"""
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/auth/me")
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
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
from jd_assistants.backend.api.v1.employees import router as employees_router
from jd_assistants.backend.api.v1.org import dept_router, pos_router

app.include_router(employees_router)
app.include_router(dept_router)
app.include_router(pos_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
