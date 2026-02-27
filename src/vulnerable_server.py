import os
from mcp.server.fastmcp import FastMCP

# WARNING: This server is for instructional purposes and contains intentional vulnerabilities (Path Traversal).
mcp = FastMCP("Vulnerable-Reference-Server")

@mcp.tool()
def read_report(filename: str):
    """
    Reference implementation of a VULNERABLE tool.
    DO NOT USE IN PRODUCTION.
    """
    # Flaw: Lack of path validation and direct concatenation
    base_dir = os.path.join(os.getcwd(), "data/reports")
    file_path = os.path.join(base_dir, filename)
    
    try:
        if not os.path.exists(file_path):
            return f"File {filename} not found."
            
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
