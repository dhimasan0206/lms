import asyncio
import logging
import os
import signal
import sys
from concurrent import futures
from pathlib import Path

import grpc

from .application.use_cases import CourseUseCases, CourseContentUseCases
from .infrastructure.repositories import SQLAlchemyCourseRepository, SQLAlchemyCourseContentRepository
from .interfaces.grpc_service import CourseGrpcService
from .config.database import async_session_factory, init_db


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


async def initialize_application():
    """Initialize application dependencies."""
    logger.info("Initializing application...")
    
    # Initialize database
    await init_db()
    
    # Create repositories
    course_repository = SQLAlchemyCourseRepository(async_session_factory)
    content_repository = SQLAlchemyCourseContentRepository(async_session_factory)
    
    # Create use cases
    course_use_cases = CourseUseCases(course_repository)
    content_use_cases = CourseContentUseCases(course_repository, content_repository)
    
    # Create gRPC service
    service = CourseGrpcService(course_use_cases, content_use_cases)
    
    return service


async def generate_proto():
    """Generate Python code from .proto file."""
    try:
        import grpc_tools.protoc as protoc
        
        proto_dir = Path(__file__).parent.parent / "proto"
        target_dir = Path(__file__).parent / "infrastructure" / "proto"
        
        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Create __init__.py file in the target directory
        with open(target_dir / "__init__.py", "w") as f:
            f.write("# Generated from proto files\n")
        
        # Get proto files
        proto_files = list(proto_dir.glob("*.proto"))
        if not proto_files:
            raise FileNotFoundError(f"No .proto files found in {proto_dir}")
            
        # Generate Python code for each proto file
        for proto_file in proto_files:
            logger.info(f"Generating Python code from {proto_file}")
            
            # Arguments for protoc
            args = [
                "grpc_tools.protoc",
                f"--proto_path={proto_dir}",
                f"--python_out={target_dir}",
                f"--grpc_python_out={target_dir}",
                str(proto_file),
            ]
            
            # Run protoc
            result = protoc.main(args)
            if result != 0:
                raise RuntimeError(f"Error generating code from {proto_file}")
                
        logger.info("Proto code generation completed.")
    except Exception as e:
        logger.error(f"Error generating proto code: {e}")
        raise


def serve():
    """Start the gRPC server."""
    # Generate proto code
    asyncio.run(generate_proto())
    
    # Get server port
    port = os.getenv("GRPC_PORT", "50051")
    server_address = f"[::]:{port}"
    
    # Get max workers
    max_workers = int(os.getenv("GRPC_MAX_WORKERS", "10"))
    
    # Create a gRPC server
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        options=[
            ("grpc.max_send_message_length", 50 * 1024 * 1024),  # 50 MB
            ("grpc.max_receive_message_length", 50 * 1024 * 1024),  # 50 MB
        ],
    )
    
    # Initialize application and add service to server
    service = asyncio.run(initialize_application())
    from .infrastructure.proto.course_pb2_grpc import add_CourseServiceServicer_to_server
    add_CourseServiceServicer_to_server(service, server)
    
    # Add port
    server.add_insecure_port(server_address)
    
    # Start server
    logger.info(f"Starting gRPC server on {server_address}")
    
    # Handle shutdown signals
    loop = asyncio.get_event_loop()
    
    async def shutdown(signal_):
        logger.info(f"Received exit signal {signal_.name}...")
        logger.info("Shutting down gRPC server...")
        await server.stop(5)  # 5 seconds grace period
        loop.stop()
        
    for s in [signal.SIGTERM, signal.SIGINT]:
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s)))
    
    # Start server and wait for termination
    async def start_server():
        await server.start()
        logger.info("Server started, waiting for termination...")
        await server.wait_for_termination()
        
    loop.run_until_complete(start_server())


if __name__ == "__main__":
    serve() 