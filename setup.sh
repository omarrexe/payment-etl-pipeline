#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# setup.sh — Bootstrap the project on any machine
# Usage: bash setup.sh
# ─────────────────────────────────────────────────────────────
set -e  # stop on any error

echo "═══════════════════════════════════════════"
echo "  Payment ETL Pipeline — Project Setup"
echo "═══════════════════════════════════════════"

# ── 1. Create virtual environment ────────────────────────────
if [ ! -d ".venv" ]; then
    echo "→ Creating virtual environment..."
    python3 -m venv .venv
else
    echo "→ Virtual environment already exists, skipping."
fi

# ── 2. Activate venv ─────────────────────────────────────────
echo "→ Activating virtual environment..."
source .venv/bin/activate

# ── 3. Install dependencies ───────────────────────────────────
echo "→ Installing dependencies from requirements.txt..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# ── 4. Create required directories ───────────────────────────
echo "→ Creating data directories..."
mkdir -p data/raw/stripe
mkdir -p data/raw/paypal
mkdir -p data/raw/bank_ach
mkdir -p data/warehouse
mkdir -p rejects
mkdir -p logs

# ── 5. Generate sample data ───────────────────────────────────
echo "→ Generating sample data for 2026-07-16..."
python src/generator/generate_data.py

echo ""
echo "✓ Setup complete!"
echo ""
echo "To activate the venv in your shell, run:"
echo "  source .venv/bin/activate"
