#!/usr/bin/env python3
"""Cross-platform MCP readiness check — run from workspace/."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path.cwd()
    starter = Path(__file__).resolve().parent.parent
    ok_count = 0
    total = 0

    def check(label: str, passed: bool, hint: str = "") -> None:
        nonlocal ok_count, total
        total += 1
        if passed:
            ok_count += 1
        suffix = f" — {hint}" if hint and not passed else ""
        print(f"{'OK' if passed else 'FAIL'}   {label}{suffix}")

    print("=== Environment ===")
    for var in ("OPENROUTER_API_KEY", "ANTHROPIC_BASE_URL", "BANKING_MCP_API_KEY"):
        check(var, bool(os.environ.get(var)))
    gh = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "")
    check("GITHUB_PERSONAL_ACCESS_TOKEN (optional)", bool(gh), "defer until github MCP")

    check("ANTHROPIC_API_KEY empty", os.environ.get("ANTHROPIC_API_KEY") == "")

    venv_py = root / ".venv" / "bin" / "python"
    check("workspace/.venv/bin/python", venv_py.is_file(), "run Step S.3 bootstrap venv")

    print("\n=== Files ===")
    for rel in (
        "CLAUDE.md",
        ".mcp.json",
        ".claude/settings.json",
        "Skills.md",
        "mcp_servers/banking_api/server.py",
    ):
        check(rel, (root / rel).exists())

    print("\n=== MCP schema ===")
    mcp_path = root / ".mcp.json"
    if mcp_path.is_file():
        try:
            sys.path.insert(0, str(starter))
            from validate_mcp_config import validate_mcp_data

            data = json.loads(mcp_path.read_text(encoding="utf-8"))
            valid, errs = validate_mcp_data(data)
            check(".mcp.json schema", valid, errs[0] if errs else "")
        except Exception as exc:
            check(".mcp.json schema", False, str(exc))
    else:
        check(".mcp.json schema", False, "copy mcp_servers_template.json")

    print("\n=== Banking API port 8080 ===")
    try:
        import urllib.request

        urllib.request.urlopen("http://localhost:8080/sse", timeout=2)
        check("SSE endpoint", True)
    except Exception:
        check("SSE endpoint", False, "python mcp_servers/banking_api/server.py")

    print("\n=== Claude Code ===")
    claude = shutil.which("claude")
    if claude:
        try:
            out = subprocess.run([claude, "--version"], capture_output=True, text=True, timeout=10)
            check("claude --version", out.returncode == 0, out.stdout.strip() or out.stderr.strip())
        except Exception as exc:
            check("claude --version", False, str(exc))
    else:
        check("claude CLI", False)

    print(f"\n{ok_count}/{total} checks passed")
    return 0 if ok_count == total else 1


if __name__ == "__main__":
    sys.exit(main())
