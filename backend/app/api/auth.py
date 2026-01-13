"""
Authentication API endpoints.
"""

from fastapi import APIRouter, HTTPException, status

from app.models.schemas import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest) -> TokenResponse:
    """
    Authenticate user and return access token.

    POST /auth/login
    """
    # TODO: Implement actual authentication with database lookup
    # This is a placeholder implementation
    # In production, verify credentials against database and generate JWT

    # Placeholder validation
    if not request.email or not request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # TODO: Generate actual JWT token
    return TokenResponse(
        access_token="placeholder_token",
        token_type="bearer",
    )
