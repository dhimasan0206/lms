from typing import Optional, Any, Dict, List


class AuthException(Exception):
    """Base exception for auth-related errors"""
    def __init__(self, message: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class InvalidCredentialsException(AuthException):
    """Exception raised when credentials are invalid"""
    def __init__(self, message: str = "Invalid credentials", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=401, details=details)


class UserNotFoundException(AuthException):
    """Exception raised when a user is not found"""
    def __init__(self, message: str = "User not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=404, details=details)


class UserAlreadyExistsException(AuthException):
    """Exception raised when a user already exists"""
    def __init__(self, message: str = "User already exists", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=409, details=details)


class TokenExpiredException(AuthException):
    """Exception raised when a token has expired"""
    def __init__(self, message: str = "Token has expired", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=401, details=details)


class InvalidTokenException(AuthException):
    """Exception raised when a token is invalid"""
    def __init__(self, message: str = "Invalid token", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=401, details=details)


class UnauthorizedException(AuthException):
    """Exception raised when a user is not authorized to perform an action"""
    def __init__(self, message: str = "Unauthorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=403, details=details)


class UserNotActiveException(AuthException):
    """Exception raised when a user account is not active"""
    def __init__(self, message: str = "User account is not active", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=403, details=details)


class PasswordPolicyException(AuthException):
    """Exception raised when a password doesn't meet policy requirements"""
    def __init__(self, message: str = "Password does not meet requirements", validation_errors: List[str] = None):
        details = {"validation_errors": validation_errors} if validation_errors else None
        super().__init__(message, status_code=400, details=details) 