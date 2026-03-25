#!/bin/bash
VENV="/home/Tanay1202/.virtualenvs/intrusion-venv"
PROJECT="/home/Tanay1202/Intrusion-Detection01"

echo "=== Step 1: Create venv ==="
python3.11 -m venv $VENV
echo "venv exit: $?"

echo "=== Step 2: Pip install ==="
$VENV/bin/pip install -q --prefer-binary Flask==2.3.3 Werkzeug==2.3.7 gunicorn==21.2.0 numpy==1.26.4 pandas==2.1.4 scikit-learn==1.3.2
echo "pip exit: $?"

echo "=== Step 3: Init DB ==="
$VENV/bin/python $PROJECT/init_db.py
echo "db exit: $?"

echo "=== SETUP COMPLETE ==="
ls $VENV/bin/python
