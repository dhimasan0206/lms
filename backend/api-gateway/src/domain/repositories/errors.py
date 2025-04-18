class RepositoryError(Exception):
    """
    Base exception class for repository errors.
    """
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error


class ServiceNotFoundError(RepositoryError):
    """
    Exception raised when a service cannot be found.
    """
    def __init__(self, service_id: str = None, service_name: str = None):
        message = "Service not found"
        if service_id:
            message += f" with ID: {service_id}"
        if service_name:
            message += f" with name: {service_name}"
        super().__init__(message)


class ServiceAlreadyExistsError(RepositoryError):
    """
    Exception raised when attempting to register a service that already exists.
    """
    def __init__(self, service_name: str):
        super().__init__(f"Service with name '{service_name}' already exists")


class ServiceHealthCheckError(RepositoryError):
    """
    Exception raised when a service health check fails.
    """
    def __init__(self, service_id: str, reason: str):
        super().__init__(f"Health check failed for service {service_id}: {reason}")


class ServiceRegistrationError(RepositoryError):
    """
    Exception raised when service registration fails.
    """
    def __init__(self, service_name: str, reason: str):
        super().__init__(f"Failed to register service '{service_name}': {reason}")


class ServiceUpdateError(RepositoryError):
    """
    Exception raised when service update fails.
    """
    def __init__(self, service_id: str, reason: str):
        super().__init__(f"Failed to update service {service_id}: {reason}")


class ServiceDeletionError(RepositoryError):
    """
    Exception raised when service deletion fails.
    """
    def __init__(self, service_id: str, reason: str):
        super().__init__(f"Failed to delete service {service_id}: {reason}") 