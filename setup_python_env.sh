#!/bin/bash

# DavidAI Python Environment Setup Script
# Run this to set up the Python dependencies for the DavidAI ecosystem

echo "Setting up DavidAI Python environment..."

# Create virtual environment
python3 -m venv davidai_env
source davidai_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "DavidAI Python environment is ready."
echo "To activate it, run: source davidai_env/bin/activate"
echo "To run the GUI, run: python gui.py"
echo "To run the CLI, run: python main.py"

