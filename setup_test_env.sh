#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install spacy model
python -m spacy download en_core_web_sm

# Run migrations
python manage.py makemigrations query_generator
python manage.py migrate

# Generate test data
python manage.py generate_test_queries 