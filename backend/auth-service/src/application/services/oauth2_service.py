import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

import httpx

from domain.entities.user import User, UserStatus, UserRole
from domain.entities.oauth2_connection import OAuth2Connection, OAuth2Provider
from domain.repositories.user_repository import UserRepository
from domain.repositories.oauth2_repository import OAuth2Repository
from application.services.auth_service import AuthService
from application.dtos.auth import SocialLoginRequest, AuthResponse, UserResponse, TokenResponse
from application.exceptions.auth_exceptions import InvalidTokenException, UserNotActiveException
from config.settings import Settings


class OAuth2Service:
    def __init__(
        self,
        user_repository: UserRepository,
        oauth2_repository: OAuth2Repository,
        auth_service: AuthService,
        settings: Settings
    ):
        self.user_repository = user_repository
        self.oauth2_repository = oauth2_repository
        self.auth_service = auth_service
        self.settings = settings
        self.http_client = httpx.AsyncClient(timeout=10.0)
    
    async def social_login(self, social_login_request: SocialLoginRequest) -> AuthResponse:
        """Login or register a user via OAuth2"""
        # Verify provider is supported
        if social_login_request.provider.value not in self.settings.OAUTH2_PROVIDERS:
            raise InvalidTokenException(f"Provider {social_login_request.provider.value} is not supported")
        
        # Verify token with provider and get user info
        provider_user_id, user_info = await self._verify_oauth2_token(
            social_login_request.provider, 
            social_login_request.access_token
        )
        
        # Check if user already has an OAuth connection
        oauth_connection = await self.oauth2_repository.get_by_provider_user_id(
            social_login_request.provider,
            provider_user_id
        )
        
        if oauth_connection:
            # User exists, update token
            oauth_connection = await self.oauth2_repository.update_tokens(
                oauth_connection.id,
                social_login_request.access_token,
                None,  # Refresh token not provided from client
                None   # Expiry not provided from client
            )
            
            # Get user
            user = await self.user_repository.get_by_id(oauth_connection.user_id)
            if not user:
                # This shouldn't happen, but just in case
                raise InvalidTokenException("User not found for existing OAuth connection")
            
            if user.status != UserStatus.ACTIVE:
                raise UserNotActiveException(f"User account is {user.status}")
            
            # Update last login
            user = await self.user_repository.update_last_login(user.id)
        else:
            # Check if user exists by email
            email = user_info.get("email")
            if not email:
                raise InvalidTokenException("OAuth provider did not provide an email address")
            
            user = await self.user_repository.get_by_email(email)
            
            if user:
                # User exists but hasn't connected this OAuth provider yet
                # Create the connection
                new_connection = OAuth2Connection(
                    id=uuid.uuid4(),
                    user_id=user.id,
                    provider=social_login_request.provider,
                    provider_user_id=provider_user_id,
                    access_token=social_login_request.access_token,
                    profile_data=user_info,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    last_used_at=datetime.utcnow()
                )
                await self.oauth2_repository.create(new_connection)
                
                if user.status != UserStatus.ACTIVE:
                    raise UserNotActiveException(f"User account is {user.status}")
                
                # Update last login
                user = await self.user_repository.update_last_login(user.id)
            else:
                # New user, register
                email_verified = user_info.get("email_verified", False)
                
                # Create user with data from OAuth provider
                new_user = User(
                    id=uuid.uuid4(),
                    email=email,
                    username=None,  # We don't get a username from OAuth providers
                    first_name=user_info.get("given_name", user_info.get("first_name", "")),
                    last_name=user_info.get("family_name", user_info.get("last_name", "")),
                    password_hash="",  # No password for OAuth users
                    roles=[UserRole.STUDENT],  # Default role
                    status=UserStatus.ACTIVE if email_verified else UserStatus.PENDING_VERIFICATION,
                    organization_id=None,
                    branch_id=None,
                    profile_image_url=user_info.get("picture"),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    email_verified=email_verified,
                    phone_verified=False
                )
                
                user = await self.user_repository.create(new_user)
                
                # Create OAuth connection
                new_connection = OAuth2Connection(
                    id=uuid.uuid4(),
                    user_id=user.id,
                    provider=social_login_request.provider,
                    provider_user_id=provider_user_id,
                    access_token=social_login_request.access_token,
                    profile_data=user_info,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    last_used_at=datetime.utcnow()
                )
                await self.oauth2_repository.create(new_connection)
        
        # Generate tokens
        device_info = social_login_request.device_info or {"source": f"oauth_{social_login_request.provider.value}"}
        token_response = await self.auth_service._generate_tokens(user, device_info)
        
        # Return response
        return AuthResponse(
            user=UserResponse.model_validate(user),
            token=token_response
        )
    
    async def _verify_oauth2_token(self, provider: OAuth2Provider, token: str) -> Tuple[str, Dict[str, Any]]:
        """Verify an OAuth2 token with the provider and return user info"""
        if provider == OAuth2Provider.GOOGLE:
            return await self._verify_google_token(token)
        elif provider == OAuth2Provider.FACEBOOK:
            return await self._verify_facebook_token(token)
        elif provider == OAuth2Provider.GITHUB:
            return await self._verify_github_token(token)
        elif provider == OAuth2Provider.APPLE:
            return await self._verify_apple_token(token)
        else:
            raise InvalidTokenException(f"Provider {provider.value} is not supported")
    
    async def _verify_google_token(self, token: str) -> Tuple[str, Dict[str, Any]]:
        """Verify a Google OAuth2 token"""
        try:
            # Google's token info endpoint
            response = await self.http_client.get(
                f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}"
            )
            response.raise_for_status()
            user_info = response.json()
            
            # Check if token is valid for our app
            if self.settings.GOOGLE_CLIENT_ID and user_info.get("aud") != self.settings.GOOGLE_CLIENT_ID:
                raise InvalidTokenException("Token not valid for this application")
            
            # Get user ID
            provider_user_id = user_info.get("sub")
            if not provider_user_id:
                raise InvalidTokenException("Could not get user ID from token")
                
            return provider_user_id, user_info
        except httpx.HTTPError:
            raise InvalidTokenException("Failed to verify Google token")
    
    async def _verify_facebook_token(self, token: str) -> Tuple[str, Dict[str, Any]]:
        """Verify a Facebook OAuth2 token"""
        try:
            # Facebook's debug token endpoint
            url = f"https://graph.facebook.com/debug_token"
            params = {
                "input_token": token,
                "access_token": f"{self.settings.FACEBOOK_CLIENT_ID}|{self.settings.FACEBOOK_CLIENT_SECRET}"
            }
            response = await self.http_client.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            
            data = result.get("data", {})
            if not data.get("is_valid", False):
                raise InvalidTokenException("Invalid Facebook token")
            
            # Check if token is valid for our app
            if self.settings.FACEBOOK_CLIENT_ID and data.get("app_id") != self.settings.FACEBOOK_CLIENT_ID:
                raise InvalidTokenException("Token not valid for this application")
            
            # Get user data
            user_id = data.get("user_id")
            if not user_id:
                raise InvalidTokenException("Could not get user ID from token")
            
            # Get user profile
            profile_url = f"https://graph.facebook.com/{user_id}"
            profile_params = {
                "fields": "id,email,first_name,last_name,picture",
                "access_token": token
            }
            profile_response = await self.http_client.get(profile_url, params=profile_params)
            profile_response.raise_for_status()
            user_info = profile_response.json()
            
            return user_id, user_info
        except httpx.HTTPError:
            raise InvalidTokenException("Failed to verify Facebook token")
    
    async def _verify_github_token(self, token: str) -> Tuple[str, Dict[str, Any]]:
        """Verify a GitHub OAuth2 token"""
        try:
            # GitHub's user endpoint
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            response = await self.http_client.get("https://api.github.com/user", headers=headers)
            response.raise_for_status()
            user_info = response.json()
            
            # Get user ID
            provider_user_id = str(user_info.get("id"))
            if not provider_user_id:
                raise InvalidTokenException("Could not get user ID from token")
            
            # Get user emails
            emails_response = await self.http_client.get(
                "https://api.github.com/user/emails",
                headers=headers
            )
            emails_response.raise_for_status()
            emails = emails_response.json()
            
            # Find primary email
            primary_email = None
            for email in emails:
                if email.get("primary", False):
                    primary_email = email
                    break
            
            if not primary_email:
                raise InvalidTokenException("Could not get primary email from GitHub account")
            
            # Add email to user info
            user_info["email"] = primary_email.get("email")
            user_info["email_verified"] = primary_email.get("verified", False)
            
            return provider_user_id, user_info
        except httpx.HTTPError:
            raise InvalidTokenException("Failed to verify GitHub token")
    
    async def _verify_apple_token(self, token: str) -> Tuple[str, Dict[str, Any]]:
        """Verify an Apple OAuth2 token"""
        # Apple token verification is more complex and requires JWT verification
        # This is a simplified version - in production you would need to verify the JWT
        try:
            # For Apple, we would normally verify the JWT token
            # This is a simplified version
            raise NotImplementedError("Apple OAuth2 verification not yet implemented")
        except Exception:
            raise InvalidTokenException("Failed to verify Apple token") 