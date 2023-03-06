#!/bin/bash
if [ -d "venv" ]; then
    echo "Removing existing virtual environment"
    rm -rf venv
fi

echo "Installing virtual environment"

python -m venv venv

echo "Activating virtual environment"

if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
elif [[ "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
else
    echo "Unsupported operating system detected: $OSTYPE"
fi

echo "Finished installation!"
