from typing import Dict, Any, Optional, List
from uuid import UUID

from domain.entities.request import Request
from domain.entities.response import Response
from domain.entities.service import Service
from domain.repositories.service_registry import ServiceRegistryRepository


class GatewayService:
    """
    Domain service for the API Gateway.
    """
    
    def __init__(self, service_registry: ServiceRegistryRepository):
        self.service_registry = service_registry
    
    async def route_request(self, request: Request) -> Response:
        """
        Route a request to the appropriate service.
        """
        # Get the service for the request path
        service = await self.service_registry.get_service_for_path(request.path)
        
        if not service:
            return Response.error(
                request_id=request.request_id,
                status_code=404,
                message=f"No service found for path: {request.path}",
            )
        
        # Check service health
        health = await self.service_registry.get_service_health(service.service_id)
        
        if not health.get("healthy", False):
            return Response.error(
                request_id=request.request_id,
                status_code=503,
                message=f"Service {service.name} is unhealthy",
            )
        
        # TODO: Implement actual request forwarding logic
        # This would involve making an HTTP request to the service
        # and handling the response
        
        # For now, return a mock response
        return Response.success(
            request_id=request.request_id,
            data={
                "service": service.name,
                "path": request.path,
                "method": request.method,
            },
            message=f"Request routed to {service.name}",
        )
    
    async def register_service(self, service_data: Dict[str, Any]) -> Service:
        """
        Register a new service.
        """
        service = Service.from_dict(service_data)
        return await self.service_registry.register_service(service)
    
    async def update_service(self, service_id: UUID, service_data: Dict[str, Any]) -> Service:
        """
        Update an existing service.
        """
        service = Service.from_dict(service_data)
        return await self.service_registry.update_service(service)
    
    async def delete_service(self, service_id: UUID) -> bool:
        """
        Delete a service.
        """
        return await self.service_registry.delete_service(service_id)
    
    async def get_service(self, service_id: UUID) -> Optional[Service]:
        """
        Get a service by ID.
        """
        return await self.service_registry.get_service(service_id)
    
    async def get_service_by_name(self, name: str) -> Optional[Service]:
        """
        Get a service by name.
        """
        return await self.service_registry.get_service_by_name(name)
    
    async def list_services(self) -> List[Service]:
        """
        List all services.
        """
        return await self.service_registry.list_services()
    
    async def check_service_health(self, service_id: UUID) -> Dict[str, Any]:
        """
        Check the health of a service.
        """
        return await self.service_registry.get_service_health(service_id) 