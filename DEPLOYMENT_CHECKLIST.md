# Deployment Checklist

## Pre-Deployment

- [ ] All dependencies listed in requirements.txt
- [ ] Database initialization script (init_db.py) tested
- [ ] Models folder included in repository
- [ ] Static files properly organized
- [ ] Secret key configured via environment variable
- [ ] Debug mode disabled (debug=False)
- [ ] Cross-platform file paths implemented
- [ ] .gitignore configured

## Platform-Specific Setup

### Render (Easiest - Recommended)
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] New Web Service created
- [ ] Build command: `pip install -r requirements.txt && python init_db.py`
- [ ] Start command: `gunicorn app:app`
- [ ] Environment variables set (if needed)

### Heroku
- [ ] Heroku CLI installed
- [ ] Heroku account created
- [ ] Procfile present
- [ ] runtime.txt present
- [ ] Git repository initialized
- [ ] App created: `heroku create app-name`
- [ ] Deployed: `git push heroku main`
- [ ] Database initialized: `heroku run python init_db.py`

### Railway
- [ ] Railway account created
- [ ] Repository connected
- [ ] Auto-deployment configured

### PythonAnywhere
- [ ] Account created
- [ ] Files uploaded
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] WSGI configuration updated
- [ ] Web app reloaded

## Post-Deployment

- [ ] Application accessible via URL
- [ ] Registration page working
- [ ] Login functionality working
- [ ] Dashboard loading correctly
- [ ] Single prediction working
- [ ] CSV upload and batch prediction working
- [ ] Static files (CSS, images) loading
- [ ] Database operations functioning
- [ ] Model predictions accurate
- [ ] No console errors

## Security Checklist

- [ ] SECRET_KEY changed from default
- [ ] Environment variables used for sensitive data
- [ ] HTTPS enabled
- [ ] SQL injection protection (parameterized queries)
- [ ] Consider password hashing implementation
- [ ] File upload validation working
- [ ] Session management secure

## Performance Checklist

- [ ] Model loading optimized
- [ ] Database queries efficient
- [ ] Static files cached
- [ ] Error handling implemented
- [ ] Logging configured

## Monitoring

- [ ] Application logs accessible
- [ ] Error tracking setup (optional)
- [ ] Uptime monitoring (optional)
- [ ] Resource usage monitored

## Troubleshooting

If deployment fails, check:
1. Python version compatibility (3.8)
2. All dependencies installed
3. Database initialized
4. File paths are cross-platform
5. PORT environment variable handled
6. Models folder included
7. Build logs for errors

## Quick Test Commands

Test locally before deploying:
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run application
python app.py
```

Visit http://localhost:5000 and test all features.
