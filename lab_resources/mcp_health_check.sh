#!/usr/bin/env bash
# Quick MCP readiness check — run from workspace/ with banking API started
set -euo pipefail

echo "=== Environment ==="
for v in OPENROUTER_API_KEY ANTHROPIC_BASE_URL BANKING_MCP_API_KEY GITHUB_PERSONAL_ACCESS_TOKEN; do
  if [[ -n "${!v:-}" ]]; then echo "OK  $v"; else echo "MISSING  $v"; fi
done

echo ""
echo "=== Files ==="
for f in CLAUDE.md .claude/settings.json Skills.md mcp_servers/banking_api/server.py; do
  [[ -e "$f" ]] && echo "OK  $f" || echo "MISSING  $f"
done

echo ""
echo "=== Banking API port 8080 ==="
if curl -sf -o /dev/null -m 2 http://localhost:8080/sse 2>/dev/null; then
  echo "OK  SSE endpoint reachable"
else
  echo "WARN  Start: python mcp_servers/banking_api/server.py"
fi

echo ""
echo "=== Claude Code ==="
claude --version 2>/dev/null || echo "MISSING  claude CLI"
