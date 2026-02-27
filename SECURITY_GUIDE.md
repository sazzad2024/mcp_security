# MCP Security Guide: Architecture & Implementation

This document outlines the security controls and architectural decisions implemented in the MCP Security project. 

## 1. Threat Model

The primary threats addressed by this implementation include:
- **Indirect Prompt Injection**: Malicious instructions embedded in data files.
- **Path Traversal**: Exploitation of filesystem utilities to access unauthorized directories.
- **Confused Deputy**: Tricking an authorized AI agent into performing unauthorized actions.
- **Resource Exhaustion (DoS)**: Intentional overloading of the server via large file requests or rapid-fire tool calls.

## 2. Security Controls

### Application Layer: Path Anchoring
The server utilizes `os.path.abspath` to resolve all symbolic links and relative segments (`../`) before validation. The resulting absolute path is then checked against a whitelist (the "Anchor") using a prefix match. This ensures that no matter how the input is encoded, it cannot resolve outside the authorized directory.

### Resource Layer: Constraints
- **File Size Capping**: A strict 1MB limit is enforced. Metadata is checked via `os.stat` before file pointers are opened, preventing memory-exhaustion attacks.
- **Rate Limiting**: A global cooldown is enforced between tool executions to mitigate automated brute-force attempts.

### System Layer: Hardening
- **Process Isolation (Sandbox)**: The macOS Seatbelt policy (`config/policy.sb`) provides a final safety net at the kernel level, denying file-read access to sensitive directories even if the Python process is compromised.
- **Containerization (Docker)**: The service is designed to run in a "Distroless-style" container where sensitive data simply does not exist in the filesystem, creating a physical "Air Gap."

## 3. Deployment Recommendations

1.  **Always use Docker**: For production workloads, the containerized deployment is the only recommended mode.
2.  **Stateless Execution**: Configure your orchestrator to recycle containers frequently to clear any potential state-based exploits.
3.  **Audit Logging**: Monitor the container logs for `Security Alert` warnings, which indicate active traversal attempts.

---
*Reference Implementation for Model Context Protocol Security.*
