#!/bin/bash
# Gillian-EMRY Hybrid Installation Script (Linux/Mac)

set -e

echo ""
echo "======================================================================="
echo "  GILLIAN-EMRY HYBRID INSTALLATION"
echo "  💯 100% LOCAL - ZERO API COSTS"
echo "======================================================================="
echo ""

# Check Python
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Please install Python 3.7+ first"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Found: $PYTHON_VERSION"

# Install Python dependencies
echo ""
echo "[2/5] Installing Python dependencies..."
echo "(This may take 2-5 minutes)"

cd gillian_server
python3 -m pip install --upgrade pip --quiet
python3 -m pip install -r requirements.txt --quiet

echo "✅ Dependencies installed"

# Download spaCy model
echo ""
echo "[3/5] Downloading spaCy language model..."
echo "(en_core_web_sm - ~12MB)"

python3 -m spacy download en_core_web_sm --quiet || {
    echo "⚠️  spaCy model download failed"
    echo "Gillian will still work with limited NLP features"
}

echo "✅ NLP ready"

# Create directories
echo ""
echo "[4/5] Creating Gillian directories..."

GILLIAN_DIR="$HOME/.gillian"
mkdir -p "$GILLIAN_DIR/memories"
mkdir -p "$GILLIAN_DIR/logs"

echo "✅ Created: $GILLIAN_DIR"

# Set up ngrok (optional)
echo ""
echo "[5/5] Checking ngrok..."

if command -v ngrok &> /dev/null; then
    echo "✅ ngrok found - wormhole ready!"
    echo ""
    echo "To use ngrok, get a free auth token:"
    echo "https://dashboard.ngrok.com/get-started/your-authtoken"
    echo ""
    echo "Then add it to gillian_server/config.json:"
    echo '  "ngrok_authtoken": "your_token_here"'
else
    echo "⚠️  ngrok not found (optional)"
    echo "Install with: pip install pyngrok"
    echo "Or download from: https://ngrok.com/download"
fi

echo ""
echo "======================================================================="
echo "  INSTALLATION COMPLETE! 🎉"
echo "======================================================================="
echo ""
echo "Features enabled:"
echo "  ✅ Local NLP (spaCy) - FREE"
echo "  ✅ SQLite Database - FREE"
echo "  ✅ Intent Detection - FREE"
echo "  ✅ British Personality - FREE"
echo "  ✅ PC Task Runner - FREE"
echo ""
echo "Next steps:"
echo "  1. Start server:  ./start_gillian.sh"
echo "  2. Start runner:  cd gillian_runner && python3 runner.py"
echo "  3. Set up iPhone Shortcut (see docs/iphone_shortcut.md)"
echo ""
echo "Your data: $GILLIAN_DIR"
echo ""
echo "Total API cost: \$0.00 forever! 💰✨"
echo ""
