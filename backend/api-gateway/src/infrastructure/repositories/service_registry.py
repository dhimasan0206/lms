from typing import Dict, List, Optional
from uuid import UUID

from domain.entities.service import Service
from domain.repositories.service_registry import ServiceRegistryRepository


class InMemoryServiceRegistryRepository(ServiceRegistryRepository):
    """
    In-memory implementation of the service registry repository.
    """
    
    def __init__(self):
        self.services: Dict[UUID, Service] = {}
    
    async def register(self, service: Service) -> Service:
        """
        Register a new service.
        """
        self.services[service.id] = service
        return service
    
    async def update(self, service_id: UUID, service_data: Dict) -> Optional[Service]:
        """
        Update an existing service.
        """
        if service_id not in self.services:
            return None
        
        service = self.services[service_id]
        updated_service = Service(
            id=service.id,
            name=service_data.get("name", service.name),
            description=service_data.get("description", service.description),
            base_url=service_data.get("base_url", service.base_url),
            health_check_url=service_data.get("health_check_url", service.health_check_url),
            is_active=service_data.get("is_active", service.is_active),
            metadata=service_data.get("metadata", service.metadata)
        )
        self.services[service_id] = updated_service
        return updated_service
    
    async def delete(self, service_id: UUID) -> bool:
        """
        Delete a service.
        """
        if service_id not in self.services:
            return False
        
        del self.services[service_id]
        return True
    
    async def get(self, service_id: UUID) -> Optional[Service]:
        """
        Get a service by ID.
        """
        return self.services.get(service_id)
    
    async def get_by_name(self, name: str) -> Optional[Service]:
        """
        Get a service by name.
        """
        for service in self.services.values():
            if service.name == name:
                return service
        return None
    
    async def list(self) -> List[Service]:
        """
        List all services.
        """
        return list(self.services.values())
    
    async def check_health(self, service_id: UUID) -> Dict:
        """
        Check the health of a service.
        """
        service = await self.get(service_id)
        if not service:
            return {
                "status": "error",
                "message": "Service not found"
            }
        
        # In a real implementation, this would make an HTTP request to the service's health check endpoint
        return {
            "status": "ok" if service.is_active else "error",
            "service_id": str(service.id),
            "service_name": service.name,
            "is_active": service.is_active
        } 