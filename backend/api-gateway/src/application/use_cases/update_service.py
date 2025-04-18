from typing import Dict, Any
from uuid import UUID

from domain.entities.service import Service
from domain.services.gateway_service import GatewayService


class UpdateServiceUseCase:
    """
    Use case for updating an existing service.
    """
    
    def __init__(self, gateway_service: GatewayService):
        self.gateway_service = gateway_service
    
    async def execute(self, service_id: UUID, service_data: Dict[str, Any]) -> Service:
        """
        Execute the use case.
        """
        return await self.gateway_service.update_service(service_id, service_data) 