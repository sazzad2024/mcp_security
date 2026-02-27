import os
import time
import logging
from mcp.server.fastmcp import FastMCP

# Configure professional logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MCP-Security")

mcp = FastMCP("Secure-Report-Server")

# Configuration Constants
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB
RATE_LIMIT_COOLDOWN = 1.0        # Seconds
last_request_time = 0.0

# Base directory anchoring
BASE_DIR = os.path.abspath(os.getcwd())
REPORTS_DIR = os.path.abspath(os.path.join(BASE_DIR, "data/reports"))

def validate_secure_path(user_filename: str) -> str:
    """
    Validates and resolves a user-provided filename against the secure root.
    Implements absolute path resolution and prefix validation (Path Anchoring).
    """
    target_path = os.path.abspath(os.path.join(REPORTS_DIR, user_filename))
    
    if not target_path.startswith(REPORTS_DIR):
        logger.warning(f"Security Alert: Unauthorized path access attempt: {user_filename}")
        raise PermissionError(f"Security Alert: Attempted access outside of sandbox: {user_filename}")
    
    return target_path

@mcp.tool()
def read_report(filename: str) -> str:
    """
    Secure tool to read reports from the authorized distribution directory.
    
    Implemented Protections:
    1. Path Anchoring (Prefix validation)
    2. Absolute Path Resolution (Traversal prevention)
    3. File Size Capping (DoS prevention)
    4. Rate Limiting (Brute-force/Automation prevention)
    """
    global last_request_time
    
    try:
        # Rate Limiting Enforcement
        current_time = time.time()
        if current_time - last_request_time < RATE_LIMIT_COOLDOWN:
            return f"Error: Rate limit exceeded. Please wait {RATE_LIMIT_COOLDOWN}s between requests."
        last_request_time = current_time

        # Path Security Validation
        safe_path = validate_secure_path(filename)
        
        # Resource Constraint Validation
        if not os.path.exists(safe_path):
            return f"Error: Report '{filename}' not found."
            
        file_size = os.path.getsize(safe_path)
        if file_size > MAX_FILE_SIZE:
             logger.error(f"Resource Denial: File {filename} exceeds {MAX_FILE_SIZE} bytes.")
             return f"Error: File '{filename}' exceeds security policy size limits."
        
        logger.info(f"Access granted: {filename} ({file_size} bytes)")
        
        with open(safe_path, "r") as f:
            return f.read()
            
    except PermissionError as pe:
        return f"Denied: {str(pe)}"
    except Exception as e:
        logger.error(f"System Error: {str(e)}")
        return f"Error: Internal system fault during processing."

if __name__ == "__main__":
    logger.info(f"MCP Security starting. Active Anchor: {REPORTS_DIR}")
    mcp.run()
