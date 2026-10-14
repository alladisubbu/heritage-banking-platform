# CLAUDE.md — Heritage National Bank AI Platform

> This document is the authoritative context for all Claude Code sessions on this codebase.
> Claude Code reads this file on every session start. Keep it accurate and concise.
> Last updated: June 2026 | Version: 1.0

---

## Platform Architecture

This repository implements Heritage National Bank's AI-powered banking platform.
Architecture follows a layered design:

```
Skills.md Library  →  MCP Tool Layer (3 servers)  →  Claude API  →  Banking Application Layer
     ↓                      ↓                            ↓                    ↓
  Skill defs           Tool execution              Haiku/Sonnet/Opus      Chatbot/Fraud/KYC
```

## Module Component Inventory

| Module | Components | Directory |
|--------|-----------|-----------|
| M1 | email-summarisation, transaction-categorisation skills | `./Skills.md` |
| M2 | Customer info MCP server (stdio), sequential pipeline | `./mcp_servers/customer_info/` |
| M3 | Banking chatbot (streaming + SSE), fraud detection (tool use) | `./chatbot/`, `./fraud_detection/` |
| M4 | Banking API MCP server (HTTP/SSE), KYC vision pipeline | `./mcp_servers/banking_api/` |
| M5 | Batch fraud engine, Claude-as-Judge, PCI DSS security layer | `./batch_processing/`, `./evaluators/` |
| M6 | Claude Code config, extended skills, CI/CD gate | `./` (this repo root) |

## Commands Reference

```bash
# Start Module 4 banking API server (must be running for MCP to work)
python mcp_servers/banking_api/server.py

# Run tests
pytest tests/ -v

# Lint check
bandit -r . --severity-level medium

# Claude Code headless mode (for CI/CD)
claude -p "prompt" --output-format stream-json
```

## Python Coding Conventions

- **Python version:** 3.10+
- **Type hints:** Required on ALL function signatures
- **Docstrings:** Google-style (Args:, Returns:, Raises: sections)
- **Error handling:** Never swallow silently — always log before re-raising
- **Secrets:** Use `python-dotenv` — NEVER hardcode credentials
- **PII in logs:** PROHIBITED. Mask card numbers (last 4 only), truncate account IDs to last 6 chars

## MCP Server Registry

Three MCP servers are registered for this codebase:

### 1. customer-info (Module 2)
- Transport: stdio | Command: `python mcp_servers/customer_info/server.py`
- Tools: `store_customer_info`, `retrieve_customer_info`
- Resources: `customer_profile` (readable JSON context)
- Auth: None (local stdio process)

### 2. banking-api (Module 4)
- Transport: HTTP/SSE | URL: `http://localhost:8080/sse`
- Tools: `get_account_balance`, `initiate_transfer`, `apply_for_loan`
- Prompt: `generate_kyc_approval_rationale`
- Auth: `X-API-Key` header → env var `BANKING_MCP_API_KEY`

### 3. github (Official Anthropic)
- Transport: stdio | Package: `@modelcontextprotocol/server-github`
- Tools: `list_repos`, `list_issues`, `create_branch`, `push_files`, `create_pull_request`
- Auth: `GITHUB_PERSONAL_ACCESS_TOKEN` env var

## Skills.md Schema

All skills MUST follow this schema exactly:

```yaml
- name: skill_name
  description: "One-line description"
  model: claude-haiku-4-5        # haiku/sonnet/opus
  system_prompt: |
    [Role + constraints]
  input_format: "Description of input"
  output_format: "JSON structure description"
  cache_control: ephemeral        # Required on all stable system prompts
```

## PCI DSS Standards — MANDATORY

Claude Code MUST NEVER generate code that violates these rules:

1. **No plaintext card data in logs** — mask to last 4 digits: `****-****-****-{last4}`
2. **No hardcoded credentials** — all secrets via environment variables
3. **Encryption at rest** — customer PII encrypted with AES-256
4. **API auth required** — all MCP HTTP endpoints require `X-API-Key` header
5. **Input sanitization** — validate ALL inputs before banking API calls
6. **Audit logging** — every tool call + financial decision → `audit_log/`
7. **Safe error messages** — NEVER expose stack traces or internal paths to clients

```python
# ✅ CORRECT
logger.info(f"Card: ****-****-****-{card[-4:]}")
api_key = os.environ.get("BANKING_API_KEY")

# ❌ WRONG — will fail bandit scan and CI gate
logger.info(f"Card: {card_number}")
api_key = "sk-live-abc123"
```

## Audit Log Configuration

| Log File | Contents | Format |
|----------|----------|--------|
| `audit_log/mcp_tool_calls.jsonl` | Every MCP tool call | JSONL |
| `audit_log/financial_decisions.jsonl` | Fraud/compliance decisions | JSONL |
| `audit_log/compliance_events.jsonl` | KYC/AML/sanctions events | JSONL |

Entry format: `{"timestamp": "ISO8601", "event_type": "...", "session_id": "...", "data": {...}}`

## Model Routing Strategy

| Task Type | Model | Rationale |
|-----------|-------|-----------|
| Balance enquiries, simple lookups | claude-haiku-4-5 | High volume, low complexity |
| Transaction analysis, compliance summaries | claude-sonnet-4-5 | Balanced quality/cost |
| Multi-document legal analysis, complex reasoning | claude-opus-4-5 | Max capability required |
