# Use a lightweight Python base image
FROM python:3.10-slim

# Set environment variables for better Python behavior in containers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-privileged user for security isolation
RUN useradd -m mcpuser
WORKDIR /home/mcpuser

# Install dependencies first (leverage Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and safe data distributions
# Note: Sensitive data is intentionally excluded from the build context
COPY --chown=mcpuser:mcpuser src/ ./src/
COPY --chown=mcpuser:mcpuser config/ ./config/
COPY --chown=mcpuser:mcpuser data/reports/ ./data/reports/

# Switch to non-root user
USER mcpuser

# Standard MCP port
EXPOSE 8000

# Execute server
CMD ["python", "src/secure_server.py"]
