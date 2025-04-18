# HTTP Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_500_INTERNAL_SERVER_ERROR = 500
HTTP_502_BAD_GATEWAY = 502
HTTP_503_SERVICE_UNAVAILABLE = 503

# Error Messages
ERROR_INVALID_CREDENTIALS = "Invalid credentials"
ERROR_UNAUTHORIZED = "Unauthorized access"
ERROR_FORBIDDEN = "Forbidden access"
ERROR_NOT_FOUND = "Resource not found"
ERROR_CONFLICT = "Resource conflict"
ERROR_VALIDATION = "Validation error"
ERROR_INTERNAL = "Internal server error"
ERROR_SERVICE_UNAVAILABLE = "Service unavailable"

# Headers
HEADER_AUTHORIZATION = "Authorization"
HEADER_TENANT_ID = "X-Tenant-ID"
HEADER_USER_ID = "X-User-ID"
HEADER_REQUEST_ID = "X-Request-ID"
HEADER_CORRELATION_ID = "X-Correlation-ID"

# Token
TOKEN_PREFIX = "Bearer"
TOKEN_EXPIRY = 30  # minutes

# Cache
CACHE_TTL = 300  # seconds
CACHE_PREFIX = "lms:api-gateway:"

# Rate Limiting
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_PERIOD = 60  # seconds

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Service Names
SERVICE_AUTH = "auth-service"
SERVICE_USER = "user-service"
SERVICE_COURSE = "course-service"
SERVICE_CONTENT = "content-service"
SERVICE_ENROLLMENT = "enrollment-service"
SERVICE_ASSESSMENT = "assessment-service"
SERVICE_BADGE = "badge-service"
SERVICE_ANALYTICS = "analytics-service"
SERVICE_NOTIFICATION = "notification-service"

# API Versions
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Timeouts
REQUEST_TIMEOUT = 30  # seconds
CONNECT_TIMEOUT = 5  # seconds 