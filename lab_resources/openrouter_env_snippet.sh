#!/usr/bin/env bash
# BYO machines only — Wipro lab already has OpenRouter in ~/.bashrc (verify: docs/LAB_PRECONFIGURED_ENV.md)
# Append to ~/.bashrc only if OPENROUTER verification fails (edit keys before sourcing)
export OPENROUTER_API_KEY="sk-or-v1-your-key"
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""
# Banking key: lab default (see docs/LAB_CREDENTIALS_SETUP.md §1)
export BANKING_MCP_API_KEY="lab-banking-key-001"
# GitHub PAT: create at https://github.com/settings/tokens (see docs/LAB_CREDENTIALS_SETUP.md §2)
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token"
