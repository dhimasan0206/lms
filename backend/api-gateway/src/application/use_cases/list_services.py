from typing import List

from domain.entities.service import Service
from domain.services.gateway_service import GatewayService


class ListServicesUseCase:
    """
    Use case for listing all services.
    """
    
    def __init__(self, gateway_service: GatewayService):
        self.gateway_service = gateway_service
    
    async def execute(self) -> List[Service]:
        """
        Execute the use case.
        """
        return await self.gateway_service.list_services() 