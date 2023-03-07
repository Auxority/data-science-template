#!/bin/bash
set -euo pipefail

trap 'printf "Aborting due to error\n"; exit 1' ERR
trap 'printf "Aborting due to signal\n"; exit 2' INT TERM

if [ ! -d "venv" ]; then
    printf "Could not find a virtual environment!\n"
    exit 1
fi

printf "Upgrading pip...\n"
python -m pip install --upgrade pip --quiet

printf "Checking for outdated dependencies...\n"
outdated=$(python -m pip list --outdated --format=columns | awk '{if(NR>2)print $1}')
if [ -n "$outdated" ]; then
    printf "Upgrading outdated dependencies...\n"
    python -m pip install --upgrade $outdated --quiet
    python -m pip freeze > setup/requirements.txt
fi

printf "Finished updating dependencies!\n"
