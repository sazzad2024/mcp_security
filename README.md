# MCP Security: Defense-in-Depth for Model Context Protocol

A professional reference implementation for securing AI agents utilizing the **Model Context Protocol (MCP)**. This repository demonstrates industry-standard security patterns to protect local systems from prompt injection, path traversal, and resource exhaustion.

## 🛡️ Security Architecture

This project implements a multi-layered defense strategy (**Defense-in-Depth**):

1.  **Application Layer**: Strict Path Anchoring and validation using absolute path resolution.
2.  **Resource Layer**: File size capping and rate limiting to prevent DoS attacks.
3.  **OS Layer**: macOS Sandbox (Seatbelt) profiles for kernel-level process restriction.
4.  **Container Layer**: Dockerized environments for total filesystem and process isolation.

## 🏗️ Project Structure

- `src/secure_server.py`: Hardened MCP server implementation featuring advanced security decorators.
- `src/vulnerable_server.py`: Instructional reference for common MCP security pitfalls.
- `config/policy.sb`: macOS-specific security policy for hardened local execution.
- `Dockerfile`: Production-ready container configuration using non-root localized users.
- `data/`: Sample data distribution directory.
- `tests/`: Automated security validation suites.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker (for containerized deployment)

### Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Secure Server
```bash
python src/secure_server.py
```

### Running with OS Hardening (macOS)
```bash
sandbox-exec -f config/policy.sb python src/secure_server.py
```

### Containerized Deployment
```bash
docker build -t mcp-sentinel .
docker run -i --rm mcp-sentinel
```

## 🧪 Security Validation

Validate the security implementation by running the included test suite:
```bash
python tests/security_audit.py
```

## 📖 Best Practices Implemented

- **Path Anchoring**: Ensures all file operations remain within a strictly defined root.
- **Least Privilege**: Services are configured to run with the minimum necessary permissions.
- **Fail-Safe Defaults**: Access is denied unless explicitly permitted by the security policy.
- **Resource Constraints**: Strict limits on memory-intensive operations.

## ⚖️ License
MIT
