#!/usr/bin/env bash
set -o errexit

# Install system dependencies for Pillow
apt-get update && apt-get install -y \
    libjpeg-dev zlib1g-dev libfreetype6-dev \
    liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Collect static and migrate
python manage.py collectstatic --noinput
python manage.py migrate --noinput