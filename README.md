# Intrusion Detection System

Network intrusion detection system using machine learning to detect unusual traffic patterns.

## Features

- Real-time network packet analysis
- Multiple attack type detection (DoS, Probe, R2L, U2R)
- Batch prediction via CSV upload
- User authentication system
- Web-based dashboard

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize database:
```bash
python init_db.py
```

3. Run the application:
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for various platforms including:
- Heroku
- Render (Recommended - Free tier)
- Railway
- PythonAnywhere
- Google Cloud Platform
- AWS Elastic Beanstalk
- DigitalOcean

### Quick Deploy to Render (Recommended)

1. Push code to GitHub
2. Go to https://render.com and create account
3. Create new Web Service from your repository
4. Configure:
   - Build Command: `pip install -r requirements.txt && python init_db.py`
   - Start Command: `gunicorn app:app`
5. Deploy!

## Technology Stack

- Python 3.8
- Flask (Web Framework)
- scikit-learn (Machine Learning)
- SQLite (Database)
- Random Forest Classifier (Model)

## Attack Types Detected

- **DoS (Denial of Service)**: Attacks that make resources unavailable
- **Probe**: Surveillance and probing attacks
- **R2L (Remote to Local)**: Unauthorized access from remote machine
- **U2R (User to Root)**: Unauthorized access to root privileges
- **Normal**: Legitimate network traffic

## Project Structure

```
├── app.py                  # Main Flask application
├── Database.py             # Database operations
├── init_db.py             # Database initialization
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment configuration
├── models/                # Trained ML models
│   └── rf_classifier.pkl
├── templates/             # HTML templates
├── static/                # CSS, images, JS
└── database/              # SQLite database
```

## Security Notes

- Change the SECRET_KEY in production
- Use environment variables for sensitive data
- Consider implementing password hashing
- Enable HTTPS in production

## License

This project is for educational purposes.

## Support

For deployment issues, see [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section.

