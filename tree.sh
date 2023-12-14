#!/bin/bash
# Navigate to the script directory or exit if it fails
cd "$(dirname "$0")" || exit

# Activate the virtual environment
source venv/bin/activate

# Run your Python script with all arguments passed in
python src/script.py "$@"

# Deactivate the virtual environment
deactivate
