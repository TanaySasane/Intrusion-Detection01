#!/bin/bash

echo "=== Intrusion Detection System - Deployment Script ==="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
fi

echo "Choose deployment platform:"
echo "1. Heroku"
echo "2. Render (via GitHub)"
echo "3. Railway"
echo "4. Local testing"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "Deploying to Heroku..."
        read -p "Enter Heroku app name: " appname
        heroku create $appname
        git push heroku main
        heroku run python init_db.py
        heroku open
        ;;
    2)
        echo "For Render deployment:"
        echo "1. Push your code to GitHub"
        echo "2. Go to https://render.com"
        echo "3. Create new Web Service from your repo"
        echo "4. Use these settings:"
        echo "   Build: pip install -r requirements.txt && python init_db.py"
        echo "   Start: gunicorn app:app"
        ;;
    3)
        echo "For Railway deployment:"
        echo "1. Go to https://railway.app"
        echo "2. Create new project from GitHub repo"
        echo "3. Railway will auto-detect and deploy"
        ;;
    4)
        echo "Setting up local environment..."
        python init_db.py
        echo "Starting application..."
        python app.py
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
