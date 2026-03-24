# Deployment Guide - Intrusion Detection System

This guide covers multiple deployment options for your Flask-based intrusion detection application.

## Prerequisites

- Python 3.8
- Git (for version control)
- Account on chosen deployment platform

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python init_db.py
```

3. Run the application:
```bash
python app.py
```

The app will be available at `http://localhost:5000`

---

## Deployment Options

### Option 1: Heroku (Recommended for beginners)

1. Install Heroku CLI:
   - Download from: https://devcenter.heroku.com/articles/heroku-cli

2. Login to Heroku:
```bash
heroku login
```

3. Create a new Heroku app:
```bash
heroku create your-app-name
```

4. Initialize git (if not already done):
```bash
git init
git add .
git commit -m "Initial commit"
```

5. Deploy to Heroku:
```bash
git push heroku main
```

6. Initialize the database on Heroku:
```bash
heroku run python init_db.py
```

7. Open your app:
```bash
heroku open
```

**Note:** Heroku's free tier has been discontinued. Consider using their paid plans or alternative platforms.

---

### Option 2: Render (Free tier available)

1. Create account at https://render.com

2. Create a new Web Service:
   - Connect your GitHub repository
   - Or use "Deploy from Git URL"

3. Configure the service:
   - **Name:** your-app-name
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt && python init_db.py`
   - **Start Command:** `gunicorn app:app`

4. Add environment variables (if needed):
   - Click "Environment" tab
   - Add any required variables

5. Click "Create Web Service"

Your app will be deployed automatically!

---

### Option 3: PythonAnywhere

1. Create account at https://www.pythonanywhere.com

2. Upload your project files:
   - Use "Files" tab to upload
   - Or clone from Git repository

3. Create a virtual environment:
```bash
mkvirtualenv --python=/usr/bin/python3.8 myenv
pip install -r requirements.txt
```

4. Initialize database:
```bash
python init_db.py
```

5. Configure Web App:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.8
   - Set source code directory
   - Edit WSGI configuration file:

```python
import sys
path = '/home/yourusername/your-project-folder'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

6. Reload the web app

---

### Option 4: Railway

1. Create account at https://railway.app

2. Create new project:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Or "Deploy from local directory"

3. Railway will auto-detect Flask app

4. Add start command in railway.json (create if needed):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python init_db.py && gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

5. Deploy automatically on push

---

### Option 5: Google Cloud Platform (App Engine)

1. Install Google Cloud SDK

2. Create app.yaml:
```yaml
runtime: python38

handlers:
- url: /static
  static_dir: static

- url: /.*
  script: auto
```

3. Deploy:
```bash
gcloud app deploy
```

---

### Option 6: AWS Elastic Beanstalk

1. Install AWS CLI and EB CLI:
```bash
pip install awsebcli
```

2. Initialize EB:
```bash
eb init -p python-3.8 your-app-name
```

3. Create environment and deploy:
```bash
eb create your-env-name
eb deploy
```

4. Open app:
```bash
eb open
```

---

### Option 7: DigitalOcean App Platform

1. Create account at https://www.digitalocean.com

2. Create new app:
   - Click "Create" → "Apps"
   - Connect GitHub repository

3. Configure:
   - **Build Command:** `pip install -r requirements.txt && python init_db.py`
   - **Run Command:** `gunicorn app:app`

4. Deploy

---

## Production Considerations

### Security Enhancements

1. Change the secret key in app.py:
```python
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
```

2. Use environment variables for sensitive data

3. Enable HTTPS (most platforms provide this automatically)

4. Hash passwords before storing (currently stored as plain text):
```python
from werkzeug.security import generate_password_hash, check_password_hash
```

### Database

- Current setup uses SQLite (file-based)
- For production, consider PostgreSQL or MySQL
- Most platforms offer managed database services

### Performance

1. Set debug=False in production:
```python
if __name__ == "__main__":
    app.run(debug=False)
```

2. Use production WSGI server (gunicorn is already configured)

3. Consider adding caching for model predictions

### Monitoring

- Enable application logging
- Set up error tracking (Sentry, Rollbar)
- Monitor resource usage

---

## Troubleshooting

### Common Issues

1. **Module not found errors:**
   - Ensure all dependencies are in requirements.txt
   - Check Python version compatibility

2. **Database errors:**
   - Run init_db.py to create tables
   - Check file permissions

3. **Model loading errors:**
   - Ensure models folder is included in deployment
   - Check file paths are cross-platform compatible

4. **Port binding issues:**
   - Most platforms set PORT environment variable
   - Update app.py if needed:
```python
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

---

## Quick Start (Render - Recommended)

1. Push code to GitHub
2. Go to https://render.com
3. Click "New +" → "Web Service"
4. Connect repository
5. Use these settings:
   - Build: `pip install -r requirements.txt && python init_db.py`
   - Start: `gunicorn app:app`
6. Click "Create Web Service"

Done! Your app will be live in minutes.
