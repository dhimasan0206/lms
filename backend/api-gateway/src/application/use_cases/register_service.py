from typing import Dict, Any
from uuid import UUID

from domain.entities.service import Service
from domain.services.gateway_service import GatewayService


class RegisterServiceUseCase:
    """
    Use case for registering a new service.
    """
    
    def __init__(self, gateway_service: GatewayService):
        self.gateway_service = gateway_service
    
    async def execute(self, service_data: Dict[str, Any]) -> Service:
        """
        Execute the use case.
        """
        return await self.gateway_service.register_service(service_data) 