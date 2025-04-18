from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime


class Request:
    """
    Request entity representing an incoming HTTP request.
    """
    
    def __init__(
        self,
        request_id: UUID,
        method: str,
        path: str,
        headers: Dict[str, str],
        query_params: Dict[str, Any],
        body: Optional[Dict[str, Any]] = None,
        tenant_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        correlation_id: Optional[UUID] = None,
        timestamp: Optional[datetime] = None,
    ):
        self.request_id = request_id
        self.method = method
        self.path = path
        self.headers = headers
        self.query_params = query_params
        self.body = body or {}
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.correlation_id = correlation_id
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the request to a dictionary.
        """
        return {
            "request_id": str(self.request_id),
            "method": self.method,
            "path": self.path,
            "headers": self.headers,
            "query_params": self.query_params,
            "body": self.body,
            "tenant_id": str(self.tenant_id) if self.tenant_id else None,
            "user_id": str(self.user_id) if self.user_id else None,
            "correlation_id": str(self.correlation_id) if self.correlation_id else None,
            "timestamp": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Request":
        """
        Create a Request instance from a dictionary.
        """
        return cls(
            request_id=UUID(data["request_id"]),
            method=data["method"],
            path=data["path"],
            headers=data["headers"],
            query_params=data["query_params"],
            body=data.get("body"),
            tenant_id=UUID(data["tenant_id"]) if data.get("tenant_id") else None,
            user_id=UUID(data["user_id"]) if data.get("user_id") else None,
            correlation_id=UUID(data["correlation_id"]) if data.get("correlation_id") else None,
            timestamp=datetime.fromisoformat(data["timestamp"]) if data.get("timestamp") else None,
        ) 