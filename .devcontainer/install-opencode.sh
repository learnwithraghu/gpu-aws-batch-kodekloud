#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
#  Install OpenCode CLI in the dev container
#  This script runs automatically via postCreateCommand
# ─────────────────────────────────────────────────────────────────
set -euo pipefail

echo "🔧 Installing OpenCode CLI..."

# Check if opencode is already installed
if command -v opencode &>/dev/null; then
    echo "✅ OpenCode is already installed: $(opencode --version 2>/dev/null || echo 'unknown')"
    exit 0
fi

# Try installing via npm (preferred for dev containers)
if command -v npm &>/dev/null; then
    echo "📦 Installing OpenCode via npm..."
    npm install -g @opencode/cli
    echo "✅ OpenCode installed successfully via npm"
    opencode --version 2>/dev/null || true
    exit 0
fi

# Fallback: use the official install script
if command -v curl &>/dev/null; then
    echo "📦 Installing OpenCode via official install script..."
    curl -fsSL https://opencode.ai/v2/install | bash
    echo "✅ OpenCode installed successfully via install script"
    exit 0
fi

echo "❌ Failed to install OpenCode: no suitable installation method found"
exit 1
