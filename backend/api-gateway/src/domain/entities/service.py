from datetime import datetime
from typing import Dict, Optional
from uuid import UUID, uuid4


class Service:
    """
    Represents a microservice in the system.
    """
    
    def __init__(
        self,
        name: str,
        version: str,
        host: str,
        port: int,
        health_check_url: str,
        is_active: bool = True,
        metadata: Optional[Dict] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Initialize a new Service instance.
        
        Args:
            name: The name of the service
            version: The version of the service
            host: The host address of the service
            port: The port number the service listens on
            health_check_url: The URL endpoint for health checks
            is_active: Whether the service is currently active
            metadata: Additional metadata about the service
            id: The unique identifier for the service
            created_at: When the service was registered
            updated_at: When the service was last updated
        """
        self.id = id or uuid4()
        self.name = name
        self.version = version
        self.host = host
        self.port = port
        self.health_check_url = health_check_url
        self.is_active = is_active
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @property
    def url(self) -> str:
        """Get the full URL of the service."""
        return f"http://{self.host}:{self.port}"
    
    def to_dict(self) -> Dict:
        """
        Convert the service to a dictionary.
        
        Returns:
            A dictionary representation of the service
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "version": self.version,
            "host": self.host,
            "port": self.port,
            "health_check_url": self.health_check_url,
            "is_active": self.is_active,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Service":
        """
        Create a Service instance from a dictionary.
        
        Args:
            data: The dictionary containing service data
            
        Returns:
            A new Service instance
        """
        return cls(
            id=UUID(data["id"]),
            name=data["name"],
            version=data["version"],
            host=data["host"],
            port=data["port"],
            health_check_url=data["health_check_url"],
            is_active=data["is_active"],
            metadata=data["metadata"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )
    
    def __eq__(self, other: object) -> bool:
        """Check if two services are equal."""
        if not isinstance(other, Service):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Get the hash of the service."""
        return hash(self.id)
    
    def __str__(self) -> str:
        """Get a string representation of the service."""
        return f"{self.name} v{self.version} ({self.url})"
    
    def get_full_url(self, path: str) -> str:
        """
        Get the full URL for a service endpoint.
        """
        return f"{self.url}/{path.lstrip('/')}"
    
    def get_health_url(self) -> str:
        """
        Get the health check URL for the service.
        """
        return self.get_full_url(self.health_check_url) 