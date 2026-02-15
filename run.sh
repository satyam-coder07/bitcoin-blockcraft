#!/bin/bash
echo "🧱 Starting BlockCraft Pro..."

# Check requirements
if python3 -c "import streamlit, numpy" &> /dev/null; then
    echo "Dependencies found."
else
    echo "Installing dependencies..."
    pip install -r requirements.txt
    pip install numpy
fi

echo "Launching Streamlit App..."
streamlit run app.py
