import json
from typing import List, Optional
from uuid import UUID

import redis
from redis.exceptions import RedisError

from domain.entities.service import Service
from domain.repositories.service_registry import ServiceRegistryRepository
from infrastructure.exceptions import RepositoryError


class RedisServiceRegistryRepository(ServiceRegistryRepository):
    """
    Redis implementation of the service registry repository.
    """
    
    def __init__(self, redis_client: redis.Redis):
        """
        Initialize the repository with a Redis client.
        
        Args:
            redis_client: The Redis client to use for storage
        """
        self.redis = redis_client
        self.service_key_prefix = "service:"
        self.service_name_index = "service_names"
    
    def _get_service_key(self, service_id: UUID) -> str:
        """Get the Redis key for a service."""
        return f"{self.service_key_prefix}{str(service_id)}"
    
    def register(self, service: Service) -> Service:
        """
        Register a new service in Redis.
        
        Args:
            service: The service to register
            
        Returns:
            The registered service with its ID
            
        Raises:
            RepositoryError: If there is an error storing the service
        """
        try:
            # Store service data
            service_data = service.to_dict()
            self.redis.set(
                self._get_service_key(service.id),
                json.dumps(service_data)
            )
            
            # Add to name index
            self.redis.hset(
                self.service_name_index,
                service.name,
                str(service.id)
            )
            
            return service
        except RedisError as e:
            raise RepositoryError(f"Failed to register service: {str(e)}")
    
    def update(self, service_id: UUID, service: Service) -> Optional[Service]:
        """
        Update an existing service in Redis.
        
        Args:
            service_id: The ID of the service to update
            service: The updated service data
            
        Returns:
            The updated service if found, None otherwise
            
        Raises:
            RepositoryError: If there is an error updating the service
        """
        try:
            # Check if service exists
            if not self.redis.exists(self._get_service_key(service_id)):
                return None
            
            # Update service data
            service_data = service.to_dict()
            self.redis.set(
                self._get_service_key(service_id),
                json.dumps(service_data)
            )
            
            # Update name index if name changed
            old_service = self.get(service_id)
            if old_service and old_service.name != service.name:
                self.redis.hdel(self.service_name_index, old_service.name)
                self.redis.hset(self.service_name_index, service.name, str(service_id))
            
            return service
        except RedisError as e:
            raise RepositoryError(f"Failed to update service: {str(e)}")
    
    def delete(self, service_id: UUID) -> bool:
        """
        Delete a service from Redis.
        
        Args:
            service_id: The ID of the service to delete
            
        Returns:
            True if the service was deleted, False otherwise
            
        Raises:
            RepositoryError: If there is an error deleting the service
        """
        try:
            # Get service to remove from name index
            service = self.get(service_id)
            if not service:
                return False
            
            # Delete service data
            self.redis.delete(self._get_service_key(service_id))
            
            # Remove from name index
            self.redis.hdel(self.service_name_index, service.name)
            
            return True
        except RedisError as e:
            raise RepositoryError(f"Failed to delete service: {str(e)}")
    
    def get(self, service_id: UUID) -> Optional[Service]:
        """
        Get a service by ID from Redis.
        
        Args:
            service_id: The ID of the service to retrieve
            
        Returns:
            The service if found, None otherwise
            
        Raises:
            RepositoryError: If there is an error retrieving the service
        """
        try:
            service_data = self.redis.get(self._get_service_key(service_id))
            if not service_data:
                return None
            
            return Service.from_dict(json.loads(service_data))
        except RedisError as e:
            raise RepositoryError(f"Failed to get service: {str(e)}")
    
    def get_by_name(self, name: str) -> Optional[Service]:
        """
        Get a service by name from Redis.
        
        Args:
            name: The name of the service to retrieve
            
        Returns:
            The service if found, None otherwise
            
        Raises:
            RepositoryError: If there is an error retrieving the service
        """
        try:
            service_id = self.redis.hget(self.service_name_index, name)
            if not service_id:
                return None
            
            return self.get(UUID(service_id.decode()))
        except RedisError as e:
            raise RepositoryError(f"Failed to get service by name: {str(e)}")
    
    def list(self) -> List[Service]:
        """
        List all registered services from Redis.
        
        Returns:
            A list of all registered services
            
        Raises:
            RepositoryError: If there is an error listing services
        """
        try:
            services = []
            for key in self.redis.scan_iter(f"{self.service_key_prefix}*"):
                service_data = self.redis.get(key)
                if service_data:
                    services.append(Service.from_dict(json.loads(service_data)))
            return services
        except RedisError as e:
            raise RepositoryError(f"Failed to list services: {str(e)}")
    
    def check_health(self, service_id: UUID) -> str:
        """
        Check the health status of a service.
        
        Args:
            service_id: The ID of the service to check
            
        Returns:
            The health status message
            
        Raises:
            RepositoryError: If there is an error checking service health
        """
        try:
            service = self.get(service_id)
            if not service:
                return "Service not found"
            
            if not service.is_active:
                return "Service is inactive"
            
            # TODO: Implement actual health check by calling service.health_check_url
            return "Service is healthy"
        except RedisError as e:
            raise RepositoryError(f"Failed to check service health: {str(e)}") 