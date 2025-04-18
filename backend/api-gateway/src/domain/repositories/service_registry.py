from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from uuid import UUID

from ..entities.service import Service


class ServiceRegistryRepository(ABC):
    """
    Abstract base class for service registry repositories.
    Defines the interface for storing and retrieving service information.
    """
    
    @abstractmethod
    def register(self, service: Service) -> Service:
        """
        Register a new service.
        
        Args:
            service: The service to register
            
        Returns:
            The registered service with updated metadata
            
        Raises:
            RepositoryError: If registration fails
        """
        pass
    
    @abstractmethod
    def update(self, service: Service) -> Service:
        """
        Update an existing service.
        
        Args:
            service: The service to update
            
        Returns:
            The updated service
            
        Raises:
            RepositoryError: If update fails or service doesn't exist
        """
        pass
    
    @abstractmethod
    def delete(self, service_id: UUID) -> None:
        """
        Delete a service.
        
        Args:
            service_id: The ID of the service to delete
            
        Raises:
            RepositoryError: If deletion fails or service doesn't exist
        """
        pass
    
    @abstractmethod
    def get(self, service_id: UUID) -> Optional[Service]:
        """
        Get a service by ID.
        
        Args:
            service_id: The ID of the service to retrieve
            
        Returns:
            The service if found, None otherwise
            
        Raises:
            RepositoryError: If retrieval fails
        """
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Service]:
        """
        Get a service by name.
        
        Args:
            name: The name of the service to retrieve
            
        Returns:
            The service if found, None otherwise
            
        Raises:
            RepositoryError: If retrieval fails
        """
        pass
    
    @abstractmethod
    def list(self) -> List[Service]:
        """
        List all registered services.
        
        Returns:
            A list of all registered services
            
        Raises:
            RepositoryError: If listing fails
        """
        pass
    
    @abstractmethod
    def check_health(self, service_id: UUID) -> bool:
        """
        Check if a service is healthy.
        
        Args:
            service_id: The ID of the service to check
            
        Returns:
            True if the service is healthy, False otherwise
            
        Raises:
            RepositoryError: If health check fails or service doesn't exist
        """
        pass

    @abstractmethod
    async def get_service_for_path(self, path: str) -> Optional[Service]:
        """
        Get a service for a specific path.
        """
        pass
    
    @abstractmethod
    async def get_service_health(self, service_id: UUID) -> Dict[str, Any]:
        """
        Get the health status of a service.
        """
        pass
    
    @abstractmethod
    async def update_service_health(self, service_id: UUID, health: Dict[str, Any]) -> None:
        """
        Update the health status of a service.
        """
        pass 