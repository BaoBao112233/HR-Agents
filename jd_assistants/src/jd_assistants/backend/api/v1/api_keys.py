"""
API Key Management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from jd_assistants.clickhouse_db import (
    create_api_key, get_user_api_keys, get_active_api_key, delete_api_key
)


router = APIRouter(prefix="/api/v1/api-keys", tags=["api-keys"])


class APIKeyCreate(BaseModel):
    provider: str  # groq, openrouter, gemini, gpt, openai
    key_name: Optional[str] = None
    api_key: str


class APIKeyResponse(BaseModel):
    id: str
    provider: str
    key_name: str
    api_key_preview: str  # Masked version
    is_active: bool
    created_at: datetime


class APIKeyListResponse(BaseModel):
    keys: List[APIKeyResponse]


def mask_api_key(key: str) -> str:
    """Mask API key for security"""
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"


# Dependency to get current user (placeholder - replace with actual auth)
async def get_current_user_id() -> str:
    # TODO: Replace with actual authentication
    # For now, return a default user ID
    return "user_1"


@router.post("/", response_model=APIKeyResponse)
async def add_api_key(
    key_data: APIKeyCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Add a new API key for the current user"""
    # Validate provider
    valid_providers = ["groq", "openrouter", "gemini", "gpt", "openai"]
    if key_data.provider.lower() not in valid_providers:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid provider. Must be one of: {', '.join(valid_providers)}"
        )
    
    # Create key
    key_dict = {
        "user_id": user_id,
        "provider": key_data.provider.lower(),
        "key_name": key_data.key_name or f"{key_data.provider} Key",
        "api_key": key_data.api_key
    }
    
    result = create_api_key(key_dict)
    
    return APIKeyResponse(
        id=result["id"],
        provider=result["provider"],
        key_name=result["key_name"],
        api_key_preview=mask_api_key(result["api_key"]),
        is_active=True,
        created_at=datetime.utcnow()
    )


@router.get("/", response_model=APIKeyListResponse)
async def list_api_keys(
    provider: Optional[str] = None,
    user_id: str = Depends(get_current_user_id)
):
    """List all API keys for the current user"""
    keys = get_user_api_keys(user_id, provider)
    
    return APIKeyListResponse(
        keys=[
            APIKeyResponse(
                id=k["id"],
                provider=k["provider"],
                key_name=k["key_name"],
                api_key_preview=mask_api_key(k["api_key"]),
                is_active=k["is_active"],
                created_at=k["created_at"]
            )
            for k in keys
        ]
    )


@router.get("/{provider}/active")
async def get_active_key(
    provider: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get the active API key for a specific provider"""
    api_key = get_active_api_key(user_id, provider)
    
    if not api_key:
        raise HTTPException(
            status_code=404,
            detail=f"No active API key found for provider: {provider}"
        )
    
    return {
        "provider": provider,
        "has_key": True,
        "preview": mask_api_key(api_key)
    }


@router.delete("/{key_id}")
async def remove_api_key(
    key_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete an API key"""
    success = delete_api_key(key_id, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")
    
    return {"message": "API key deleted successfully"}


@router.get("/providers/list")
async def list_providers():
    """List all supported LLM providers"""
    return {
        "providers": [
            {
                "id": "groq",
                "name": "Groq",
                "description": "Fast inference with Llama models",
                "default_model": "llama-3.3-70b-versatile",
                "models": [
                    "llama-3.3-70b-versatile",
                    "llama-3.1-70b-versatile",
                    "mixtral-8x7b-32768"
                ]
            },
            {
                "id": "openrouter",
                "name": "OpenRouter",
                "description": "Access to multiple models via one API",
                "default_model": "anthropic/claude-3.5-sonnet",
                "models": [
                    "anthropic/claude-3.5-sonnet",
                    "openai/gpt-4-turbo",
                    "google/gemini-pro"
                ]
            },
            {
                "id": "gemini",
                "name": "Google Gemini",
                "description": "Google's multimodal AI model",
                "default_model": "gemini-1.5-pro",
                "models": [
                    "gemini-1.5-pro",
                    "gemini-1.5-flash",
                    "gemini-pro"
                ]
            },
            {
                "id": "openai",
                "name": "OpenAI GPT",
                "description": "OpenAI's GPT models",
                "default_model": "gpt-4o",
                "models": [
                    "gpt-4o",
                    "gpt-4-turbo",
                    "gpt-4",
                    "gpt-3.5-turbo"
                ]
            }
        ]
    }
