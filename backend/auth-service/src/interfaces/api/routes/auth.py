from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm

from application.dtos.auth import (
    RegisterRequest, 
    AuthResponse, 
    TokenResponse, 
    UserResponse,
    RefreshTokenRequest,
    ResetPasswordRequest,
    ConfirmResetPasswordRequest,
    VerifyEmailRequest
)
from application.services.auth_service import AuthService
from application.exceptions.auth_exceptions import AuthException
from interfaces.api.dependencies import get_auth_service, require_authenticated

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post("/login", response_model=AuthResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Login with username and password (OAuth2 compatible)"""
    try:
        from application.dtos.auth import LoginRequest
        login_request = LoginRequest(
            email=form_data.username,  # OAuth2 spec uses 'username' field
            password=form_data.password
        )
        return await auth_service.login(login_request)
    except AuthException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", response_model=AuthResponse)
async def register(
    register_request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user"""
    try:
        return await auth_service.register(register_request)
    except AuthException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Refresh an access token using a refresh token"""
    try:
        return await auth_service.refresh_token(refresh_request)
    except AuthException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/reset-password", status_code=status.HTTP_202_ACCEPTED)
async def reset_password(
    reset_request: ResetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Request a password reset"""
    # Always return success to prevent email enumeration
    await auth_service.reset_password(reset_request)
    return {"status": "success", "message": "If the email exists, a password reset link has been sent"}


@router.post("/reset-password/confirm", status_code=status.HTTP_200_OK)
async def confirm_reset_password(
    reset_confirm: ConfirmResetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Confirm a password reset"""
    try:
        await auth_service.confirm_reset_password(reset_confirm)
        return {"status": "success", "message": "Password has been reset successfully"}
    except AuthException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(
    verify_request: VerifyEmailRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Verify a user's email"""
    try:
        await auth_service.verify_email(verify_request)
        return {"status": "success", "message": "Email has been verified successfully"}
    except AuthException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user = Depends(require_authenticated)
):
    """Get the current user's profile"""
    return UserResponse.model_validate(user) 