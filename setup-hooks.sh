#!/usr/bin/env bash
# Install and set up pre-commit hooks

set -e

echo "🔧 Setting up pre-commit hooks..."

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first."
    exit 1
fi

# Install dependencies if needed
if [ ! -d ".venv" ]; then
    echo "📦 Installing dependencies..."
    uv sync --group dev
fi

# Install pre-commit
echo "📦 Installing pre-commit..."
uv pip install pre-commit

# Set up pre-commit hooks
echo "🔐 Installing git hooks..."
uv run pre-commit install

echo "✅ Pre-commit hooks installed!"
echo ""
echo "Hooks will automatically run on git commit."
echo "To run manually: uv run pre-commit run --all-files"
