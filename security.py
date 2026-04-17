from fastapi import Request, HTTPException, Security
from fastapi.security import APIKeyHeader, APIKeyQuery
from slowapi import Limiter
from slowapi.util import get_remote_address
from config import Config
from typing import Optional
import time

# Rate limiter instance
limiter = Limiter(key_func=get_remote_address)

# API Key Security - Support both Header and Query
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)

# In-memory session store
session_store = {}

def verify_api_key(
    api_key_h: Optional[str] = Security(api_key_header),
    api_key_q: Optional[str] = Security(api_key_query)
):
    # Check if either provided key matches the Config.API_KEY
    if api_key_h == Config.API_KEY or api_key_q == Config.API_KEY:
        return Config.API_KEY
        
    raise HTTPException(
        status_code=403,
        detail="Could not validate credentials - Invalid API Key"
    )

def track_session(api_key: str):
    """
    Simple in-memory session tracking for API usage.
    """
    if api_key not in session_store:
        session_store[api_key] = {"usage_count": 0, "last_accessed": time.time()}
    
    session_store[api_key]["usage_count"] += 1
    session_store[api_key]["last_accessed"] = time.time()
    return session_store[api_key]
