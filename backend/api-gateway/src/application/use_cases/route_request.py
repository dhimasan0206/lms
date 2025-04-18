from typing import Dict, Any
from uuid import UUID

from domain.entities.request import Request
from domain.entities.response import Response
from domain.services.gateway_service import GatewayService


class RouteRequestUseCase:
    """
    Use case for routing a request to the appropriate service.
    """
    
    def __init__(self, gateway_service: GatewayService):
        self.gateway_service = gateway_service
    
    async def execute(
        self,
        request_id: UUID,
        method: str,
        path: str,
        headers: Dict[str, str],
        query_params: Dict[str, Any],
        body: Dict[str, Any],
        tenant_id: UUID = None,
        user_id: UUID = None,
        correlation_id: UUID = None,
    ) -> Response:
        """
        Execute the use case.
        """
        # Create a request entity
        request = Request(
            request_id=request_id,
            method=method,
            path=path,
            headers=headers,
            query_params=query_params,
            body=body,
            tenant_id=tenant_id,
            user_id=user_id,
            correlation_id=correlation_id,
        )
        
        # Route the request
        return await self.gateway_service.route_request(request) 