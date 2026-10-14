# BYO Windows only — Wipro lab: verify pre-configured env (docs/LAB_PRECONFIGURED_ENV.md)
# Add to PowerShell profile only if missing: notepad $PROFILE
$env:OPENROUTER_API_KEY = "sk-or-v1-your-key"
$env:ANTHROPIC_BASE_URL = "https://openrouter.ai/api"
$env:ANTHROPIC_AUTH_TOKEN = $env:OPENROUTER_API_KEY
$env:ANTHROPIC_API_KEY = ""
$env:BANKING_MCP_API_KEY = "lab-banking-key-001"
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "ghp_your_token"
