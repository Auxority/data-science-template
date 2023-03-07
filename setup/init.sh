#!/bin/bash
set -euo pipefail

trap 'printf "Aborting due to error\n"; exit 1' ERR
trap 'printf "Aborting due to signal\n"; exit 2' INT TERM

if [ -d "venv" ]; then
    printf "Removing existing virtual environment...\n"
    rm -rf venv
fi

printf "Installing virtual environment...\n"
python -m venv venv
if [ ! -d "venv" ]; then
    printf "Failed to create virtual environment!\n"
    exit 1
fi

printf "Activating virtual environment...\n"
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
elif [[ "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
else
    printf "Failed to install! Unsupported operating system detected: %s\n" "$OSTYPE"
    exit 1
fi

printf "Upgrading pip...\n"
python -m pip install --upgrade pip --quiet

printf "Installing dependencies...\n"
if [ ! -f "setup/requirements.txt" ]; then
    printf "Error: requirements.txt file not found!\n"
    exit 1
fi
pip install -r setup/requirements.txt --quiet

printf "Checking for outdated dependencies...\n"
outdated=$(python -m pip list --outdated --format=columns | awk '{if(NR>2)print $1}')
if [ -n "$outdated" ]; then
    printf "Upgrading outdated dependencies...\n"
    python -m pip install --upgrade $outdated --quiet
    python -m pip freeze > setup/requirements.txt
fi

printf "Finished installation!\n"
