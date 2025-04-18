from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime


class Response:
    """
    Response entity representing an outgoing HTTP response.
    """
    
    def __init__(
        self,
        request_id: UUID,
        status_code: int,
        body: Dict[str, Any],
        headers: Dict[str, str],
        error: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
    ):
        self.request_id = request_id
        self.status_code = status_code
        self.body = body
        self.headers = headers
        self.error = error
        self.metadata = metadata or {}
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the response to a dictionary.
        """
        return {
            "request_id": str(self.request_id),
            "status_code": self.status_code,
            "body": self.body,
            "headers": self.headers,
            "error": self.error,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Response":
        """
        Create a Response instance from a dictionary.
        """
        return cls(
            request_id=UUID(data["request_id"]),
            status_code=data["status_code"],
            body=data["body"],
            headers=data["headers"],
            error=data.get("error"),
            metadata=data.get("metadata"),
            timestamp=datetime.fromisoformat(data["timestamp"]) if data.get("timestamp") else None,
        )
    
    @classmethod
    def success(
        cls,
        request_id: UUID,
        data: Any,
        message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Response":
        """
        Create a success response.
        """
        body = {
            "success": True,
            "data": data,
        }
        
        if message:
            body["message"] = message
        
        return cls(
            request_id=request_id,
            status_code=200,
            body=body,
            headers={},
            metadata=metadata,
        )
    
    @classmethod
    def error(
        cls,
        request_id: UUID,
        status_code: int,
        message: str,
        errors: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Response":
        """
        Create an error response.
        """
        error = {
            "message": message,
        }
        
        if errors:
            error["errors"] = errors
        
        return cls(
            request_id=request_id,
            status_code=status_code,
            body={"success": False},
            headers={},
            error=error,
            metadata=metadata,
        ) 