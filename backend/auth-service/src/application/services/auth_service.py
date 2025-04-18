from datetime import datetime, timedelta
import uuid
from typing import Optional, Dict, Any, Tuple

from passlib.context import CryptContext
from jose import jwt, JWTError

from domain.entities.user import User, UserStatus, UserRole
from domain.entities.token import Token, TokenType
from domain.repositories.user_repository import UserRepository
from domain.repositories.token_repository import TokenRepository
from application.dtos.auth import (
    LoginRequest, 
    RegisterRequest, 
    AuthResponse, 
    TokenResponse, 
    UserResponse,
    RefreshTokenRequest,
    ResetPasswordRequest,
    ConfirmResetPasswordRequest,
    VerifyEmailRequest
)
from application.exceptions.auth_exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
    TokenExpiredException,
    InvalidTokenException,
    UserNotActiveException
)
from config.settings import Settings


class AuthService:
    def __init__(
        self, 
        user_repository: UserRepository,
        token_repository: TokenRepository,
        settings: Settings
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.settings = settings
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def _get_password_hash(self, password: str) -> str:
        """Hash a password for storing"""
        return self.pwd_context.hash(password)
    
    def _create_token(self, data: Dict[str, Any], expires_delta: timedelta) -> str:
        """Create a JWT token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            self.settings.SECRET_KEY, 
            algorithm=self.settings.JWT_ALGORITHM
        )
        return encoded_jwt
    
    def _verify_token(self, token: str, token_type: str) -> Dict[str, Any]:
        """Verify a JWT token"""
        try:
            payload = jwt.decode(
                token, 
                self.settings.SECRET_KEY, 
                algorithms=[self.settings.JWT_ALGORITHM]
            )
            if payload.get("type") != token_type:
                raise InvalidTokenException("Invalid token type")
            return payload
        except JWTError:
            raise InvalidTokenException("Invalid token")
    
    async def login(self, login_request: LoginRequest) -> AuthResponse:
        """Login a user with email and password"""
        user = await self.user_repository.get_by_email(login_request.email)
        if not user:
            raise InvalidCredentialsException("Invalid email or password")
        
        if not self._verify_password(login_request.password, user.password_hash):
            raise InvalidCredentialsException("Invalid email or password")
        
        if user.status != UserStatus.ACTIVE:
            raise UserNotActiveException(f"User account is {user.status}")
        
        # Update last login
        user = await self.user_repository.update_last_login(user.id)
        
        # Generate tokens
        token_response = await self._generate_tokens(user, login_request.device_info)
        
        return AuthResponse(
            user=UserResponse.model_validate(user),
            token=token_response
        )
    
    async def register(self, register_request: RegisterRequest) -> AuthResponse:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(register_request.email)
        if existing_user:
            raise UserAlreadyExistsException("User with this email already exists")
        
        if register_request.username:
            existing_username = await self.user_repository.get_by_username(register_request.username)
            if existing_username:
                raise UserAlreadyExistsException("User with this username already exists")
        
        # Create user
        new_user = User(
            id=uuid.uuid4(),
            email=register_request.email,
            username=register_request.username,
            first_name=register_request.first_name,
            last_name=register_request.last_name,
            password_hash=self._get_password_hash(register_request.password),
            roles=[UserRole.STUDENT],  # Default role
            status=UserStatus.PENDING_VERIFICATION,
            organization_id=register_request.organization_id,
            branch_id=register_request.branch_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            phone_number=register_request.phone_number,
            email_verified=False,
            phone_verified=False
        )
        
        created_user = await self.user_repository.create(new_user)
        
        # Generate tokens
        device_info = {"source": "registration"}
        token_response = await self._generate_tokens(created_user, device_info)
        
        # Send verification email (this would be handled by a notification service)
        # await self._send_verification_email(created_user)
        
        return AuthResponse(
            user=UserResponse.model_validate(created_user),
            token=token_response
        )
    
    async def refresh_token(self, refresh_request: RefreshTokenRequest) -> TokenResponse:
        """Refresh an access token using a refresh token"""
        # Verify refresh token exists and is valid
        token = await self.token_repository.get_by_value(refresh_request.refresh_token)
        if not token or token.token_type != TokenType.REFRESH:
            raise InvalidTokenException("Invalid refresh token")
        
        if token.expires_at < datetime.utcnow() or token.revoked:
            await self.token_repository.revoke(token.id)
            raise TokenExpiredException("Refresh token has expired")
        
        # Verify JWT
        try:
            payload = self._verify_token(token.token_value, "refresh")
            user_id = uuid.UUID(payload.get("sub"))
        except (InvalidTokenException, ValueError):
            await self.token_repository.revoke(token.id)
            raise InvalidTokenException("Invalid refresh token")
        
        # Get user
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            await self.token_repository.revoke(token.id)
            raise UserNotFoundException("User not found")
        
        if user.status != UserStatus.ACTIVE:
            await self.token_repository.revoke(token.id)
            raise UserNotActiveException(f"User account is {user.status}")
        
        # Generate new tokens
        device_info = token.device_info if token.device_info else {}
        new_token_response = await self._generate_tokens(user, device_info)
        
        # Revoke old refresh token
        await self.token_repository.revoke(token.id)
        
        return new_token_response
    
    async def reset_password(self, reset_request: ResetPasswordRequest) -> bool:
        """Request a password reset"""
        user = await self.user_repository.get_by_email(reset_request.email)
        if not user:
            # We don't want to reveal if a user exists or not
            return True
        
        # Generate reset token
        token_data = {
            "sub": str(user.id),
            "type": "reset_password",
            "jti": str(uuid.uuid4())
        }
        token_value = self._create_token(
            token_data, 
            timedelta(hours=24)  # Reset tokens valid for 24 hours
        )
        
        # Store token
        reset_token = Token(
            id=uuid.uuid4(),
            user_id=user.id,
            token_type=TokenType.RESET_PASSWORD,
            token_value=token_value,
            expires_at=datetime.utcnow() + timedelta(hours=24),
            created_at=datetime.utcnow(),
            revoked=False
        )
        await self.token_repository.create(reset_token)
        
        # Send reset email (this would be handled by a notification service)
        # await self._send_reset_email(user, token_value)
        
        return True
    
    async def confirm_reset_password(self, reset_confirm: ConfirmResetPasswordRequest) -> bool:
        """Confirm a password reset using a token"""
        # Verify token
        try:
            payload = self._verify_token(reset_confirm.token, "reset_password")
            user_id = uuid.UUID(payload.get("sub"))
            jti = payload.get("jti")
        except (InvalidTokenException, ValueError):
            raise InvalidTokenException("Invalid reset token")
        
        # Check if token exists in database
        token = await self.token_repository.get_by_value(reset_confirm.token)
        if not token or token.token_type != TokenType.RESET_PASSWORD:
            raise InvalidTokenException("Invalid reset token")
        
        if token.expires_at < datetime.utcnow() or token.revoked:
            await self.token_repository.revoke(token.id)
            raise TokenExpiredException("Reset token has expired")
        
        # Get user
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            await self.token_repository.revoke(token.id)
            raise UserNotFoundException("User not found")
        
        # Update password
        password_hash = self._get_password_hash(reset_confirm.new_password)
        await self.user_repository.update_password(user.id, password_hash)
        
        # Revoke token
        await self.token_repository.revoke(token.id)
        
        # Revoke all refresh tokens for user
        await self.token_repository.revoke_all_for_user(user.id, TokenType.REFRESH)
        
        return True
    
    async def verify_email(self, verify_request: VerifyEmailRequest) -> bool:
        """Verify a user's email using a token"""
        # Verify token
        try:
            payload = self._verify_token(verify_request.token, "email_verification")
            user_id = uuid.UUID(payload.get("sub"))
        except (InvalidTokenException, ValueError):
            raise InvalidTokenException("Invalid verification token")
        
        # Check if token exists in database
        token = await self.token_repository.get_by_value(verify_request.token)
        if not token or token.token_type != TokenType.EMAIL_VERIFICATION:
            raise InvalidTokenException("Invalid verification token")
        
        if token.expires_at < datetime.utcnow() or token.revoked:
            await self.token_repository.revoke(token.id)
            raise TokenExpiredException("Verification token has expired")
        
        # Get user
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            await self.token_repository.revoke(token.id)
            raise UserNotFoundException("User not found")
        
        # Mark email as verified
        await self.user_repository.verify_email(user.id)
        
        # If user was pending verification, set to active
        if user.status == UserStatus.PENDING_VERIFICATION:
            await self.user_repository.update_status(user.id, UserStatus.ACTIVE)
        
        # Revoke token
        await self.token_repository.revoke(token.id)
        
        return True
    
    async def _generate_tokens(self, user: User, device_info: Optional[Dict[str, Any]] = None) -> TokenResponse:
        """Generate access and refresh tokens for a user"""
        # Create access token
        access_token_data = {
            "sub": str(user.id),
            "email": user.email,
            "roles": [role.value for role in user.roles],
            "org_id": str(user.organization_id) if user.organization_id else None,
            "branch_id": str(user.branch_id) if user.branch_id else None,
            "type": "access"
        }
        access_token = self._create_token(
            access_token_data, 
            self.settings.ACCESS_TOKEN_EXPIRE_DELTA
        )
        
        # Create refresh token
        refresh_token_data = {
            "sub": str(user.id),
            "jti": str(uuid.uuid4()),
            "type": "refresh"
        }
        refresh_token = self._create_token(
            refresh_token_data, 
            self.settings.REFRESH_TOKEN_EXPIRE_DELTA
        )
        
        # Store refresh token in database
        token_entity = Token(
            id=uuid.uuid4(),
            user_id=user.id,
            token_type=TokenType.REFRESH,
            token_value=refresh_token,
            expires_at=datetime.utcnow() + self.settings.REFRESH_TOKEN_EXPIRE_DELTA,
            created_at=datetime.utcnow(),
            revoked=False,
            device_info=device_info or {}
        )
        await self.token_repository.create(token_entity)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ) 