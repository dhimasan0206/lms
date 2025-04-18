from typing import Dict, Any
from uuid import UUID

from domain.services.gateway_service import GatewayService


class CheckServiceHealthUseCase:
    """
    Use case for checking the health of a service.
    """
    
    def __init__(self, gateway_service: GatewayService):
        self.gateway_service = gateway_service
    
    async def execute(self, service_id: UUID) -> Dict[str, Any]:
        """
        Execute the use case.
        """
        return await self.gateway_service.check_service_health(service_id) 