#!/bin/bash

# MNIST ANN Setup Script
# This script sets up a virtual environment and installs all dependencies

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

echo "🚀 Setting up MNIST ANN Project..."
echo "Project directory: $PROJECT_DIR"
echo ""

# Check if virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo "✅ Virtual environment already exists at $VENV_DIR"
else
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -eq 0 ]; then
        echo "✅ Virtual environment created successfully"
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

echo ""
echo "🔧 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip setuptools wheel -q
pip install -r "$PROJECT_DIR/requirements.txt" -q

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Activate the environment: source $VENV_DIR/bin/activate"
echo "2. Start Jupyter: jupyter notebook"
echo "3. Open: mnist_ann.ipynb"
echo ""
echo "📊 Verify installation:"
echo "   python -c \"import numpy, pandas, matplotlib; print('✅ All packages imported successfully')\""
echo ""
