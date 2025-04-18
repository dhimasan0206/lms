from uuid import UUID

from domain.services.gateway_service import GatewayService


class DeleteServiceUseCase:
    """
    Use case for deleting a service.
    """
    
    def __init__(self, gateway_service: GatewayService):
        self.gateway_service = gateway_service
    
    async def execute(self, service_id: UUID) -> bool:
        """
        Execute the use case.
        """
        return await self.gateway_service.delete_service(service_id) 