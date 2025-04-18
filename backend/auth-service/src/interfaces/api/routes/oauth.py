from fastapi import APIRouter, Depends, HTTPException, status

from application.dtos.auth import SocialLoginRequest, AuthResponse
from application.services.oauth2_service import OAuth2Service
from application.exceptions.auth_exceptions import AuthException
from interfaces.api.dependencies import get_oauth2_service, require_authenticated

router = APIRouter(
    prefix="/oauth",
    tags=["oauth"],
)


@router.post("/login", response_model=AuthResponse)
async def social_login(
    social_login_request: SocialLoginRequest,
    oauth2_service: OAuth2Service = Depends(get_oauth2_service)
):
    """Login with an OAuth2 provider"""
    try:
        return await oauth2_service.social_login(social_login_request)
    except AuthException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except NotImplementedError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Login with {social_login_request.provider} not implemented yet"
        ) 