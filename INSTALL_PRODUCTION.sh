#!/bin/bash
# ============================================================================
# GILLIAN AI - PRODUCTION INSTALLATION SCRIPT
# Installs all dependencies and sets up the PWA
# ============================================================================

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║               GILLIAN AI - PRODUCTION INSTALLATION                ║"
echo "║         100% Local | Zero API Costs | Industry Standard           ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Please install Python 3.7+ first"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Found: $PYTHON_VERSION"

# Install core dependencies
echo ""
echo "[2/6] Installing Python dependencies..."
echo "(This may take 2-5 minutes)"

python3 -m pip install --user --upgrade pip setuptools wheel
python3 -m pip install --user flask flask-cors

echo "✅ Core dependencies installed"

# Try to install optional dependencies
echo ""
echo "[3/6] Installing optional NLP dependencies (spaCy)..."
python3 -m pip install --user spacy || echo "⚠️  spaCy optional - continuing..."

if command -v python3 -m spacy &> /dev/null; then
    python3 -m spacy download en_core_web_sm || echo "⚠️  Language model optional"
fi

# Create directories
echo ""
echo "[4/6] Creating application directories..."

GILLIAN_DIR="$HOME/.gillian"
mkdir -p "$GILLIAN_DIR/logs"
mkdir -p "$GILLIAN_DIR/backups"

echo "✅ Created: $GILLIAN_DIR"

# Generate placeholder icons
echo ""
echo "[5/6] Setting up PWA assets..."

mkdir -p pwa/icons

# Create simple SVG icon (will be converted to PNG by browser)
cat > pwa/icons/icon.svg << 'EOF'
<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6C63FF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#00D4FF;stop-opacity:1" />
    </linearGradient>
  </defs>
  <circle cx="256" cy="256" r="256" fill="url(#grad)"/>
  <text x="256" y="330" font-size="280" fill="white" text-anchor="middle" font-weight="bold" font-family="Arial">G</text>
</svg>
EOF

# Copy placeholder for PNG icons
cp pwa/icons/icon.svg pwa/icons/icon-192.png 2>/dev/null || true
cp pwa/icons/icon.svg pwa/icons/icon-512.png 2>/dev/null || true

echo "✅ PWA assets ready"

# Set permissions
echo ""
echo "[6/6] Setting permissions..."

chmod +x gillian_server/gillian_advanced.py
chmod +x gillian_runner/runner.py 2>/dev/null || true

echo "✅ Permissions set"

# Done!
echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║                     INSTALLATION COMPLETE! 🎉                     ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 QUICK START:"
echo ""
echo "   1. Start the server:"
echo "      ./START.sh"
echo ""
echo "   2. Open your browser:"
echo "      http://localhost:8770"
echo ""
echo "   3. On mobile, tap 'Add to Home Screen' for PWA install"
echo ""
echo "📊 FEATURES:"
echo "   ✅ Advanced AI with learning capabilities"
echo "   ✅ Voice input in browser (Web Speech API)"
echo "   ✅ Text-to-speech responses (British accent)"
echo "   ✅ Beautiful responsive UI"
echo "   ✅ Offline support (PWA)"
echo "   ✅ Zero API costs forever"
echo ""
echo "💾 DATA LOCATION:"
echo "   $GILLIAN_DIR"
echo ""
echo "📚 NEXT STEPS:"
echo "   - Customize: Edit gillian_server/gillian_advanced.py"
echo "   - Docs: See README.md"
echo ""
echo "Welcome to the future of personal AI! 🚀✨"
echo ""
