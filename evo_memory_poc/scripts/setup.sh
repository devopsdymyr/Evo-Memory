#!/bin/bash
# Setup script for Evo-Memory POC

set -e

echo "🚀 Setting up Evo-Memory POC Environment"
echo "=========================================="

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file template..."
    cat > .env << EOF
# LLM Configuration
# OPENAI_API_KEY=your_openai_key_here
# ANTHROPIC_API_KEY=your_anthropic_key_here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini

# Use mock LLM if no API keys (set to true for testing)
USE_MOCK_LLM=true
EOF
    echo "✅ Created .env file. Add your API keys if you have them."
else
    echo "✅ .env file already exists"
fi

# Create directories
mkdir -p logs
mkdir -p data

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. (Optional) Add API keys to .env file"
echo "3. Test business logic: python3 scripts/test_api_endpoints.py"
echo "4. Start API server: python3 main.py"
echo "5. Test HTTP API: python3 scripts/test_api_server.py"
echo "6. View API docs: http://localhost:8000/docs"

