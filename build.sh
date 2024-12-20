#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
python -m pip install --upgrade pip

# Install system dependencies
apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev

# Install Python packages
pip install --upgrade setuptools wheel
pip install -r requirements.txt 