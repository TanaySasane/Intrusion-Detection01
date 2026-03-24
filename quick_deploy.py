#!/usr/bin/env python3
"""
One-Click Deployment Script
Automates deployment to various platforms
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False

def check_git():
    """Check if git is initialized"""
    return os.path.exists('.git')

def deploy_heroku():
    """Deploy to Heroku"""
    print("\n🚀 Deploying to Heroku...")
    
    app_name = input("Enter Heroku app name (or press Enter for auto-generated): ").strip()
    
    if not run_command("heroku --version", "Checking Heroku CLI"):
        print("❌ Heroku CLI not installed. Install from: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    if not run_command("heroku login", "Logging into Heroku"):
        return False
    
    create_cmd = f"heroku create {app_name}" if app_name else "heroku create"
    if not run_command(create_cmd, "Creating Heroku app"):
        return False
    
    if not run_command("git push heroku master", "Pushing to Heroku"):
        return False
    
    if not run_command("heroku run python init_db.py", "Initializing database"):
        return False
    
    run_command("heroku open", "Opening app in browser")
    print("\n✅ Deployed to Heroku successfully!")
    return True

def deploy_docker():
    """Deploy using Docker"""
    print("\n🐳 Deploying with Docker...")
    
    if not run_command("docker --version", "Checking Docker"):
        print("❌ Docker not installed. Install from: https://www.docker.com/get-started")
        return False
    
    if not run_command("docker-compose build", "Building Docker image"):
        return False
    
    if not run_command("docker-compose up -d", "Starting containers"):
        return False
    
    print("\n✅ Docker deployment successful!")
    print("🌐 App running at: http://localhost:5000")
    return True

def test_local():
    """Test application locally"""
    print("\n🧪 Testing application locally...")
    
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    if not run_command("python init_db.py", "Initializing database"):
        return False
    
    print("\n✅ Setup complete!")
    print("🌐 Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    try:
        subprocess.run(["python", "app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
    
    return True

def show_instructions():
    """Show deployment instructions"""
    print("""
╔════════════════════════════════════════════════════════════╗
║         INTRUSION DETECTION SYSTEM - DEPLOYMENT            ║
╚════════════════════════════════════════════════════════════╝

📋 Quick Deployment Options:

1. 🌐 Render (Easiest - Free Tier)
   → Go to: https://render.com
   → Connect GitHub repo
   → Auto-deploys from render.yaml
   
2. 🚂 Railway (Fastest)
   → Go to: https://railway.app
   → Deploy from GitHub
   → Auto-detects configuration
   
3. 🐳 Docker (Local/Cloud)
   → Run: docker-compose up -d
   → Works on any Docker platform
   
4. 🔷 Heroku (Classic)
   → Automated via this script
   
5. 🧪 Local Testing
   → Test before deploying

📚 Full documentation: DEPLOYMENT.md
🚀 Quick guide: AUTO_DEPLOY.md
    """)

def main():
    """Main deployment menu"""
    show_instructions()
    
    print("\nSelect deployment option:")
    print("1. Deploy to Heroku (automated)")
    print("2. Deploy with Docker (local)")
    print("3. Test locally")
    print("4. Show deployment instructions")
    print("5. Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if not check_git():
        print("\n⚠️  Git not initialized. Initializing...")
        run_command("git init", "Initializing git")
        run_command("git add .", "Adding files")
        run_command('git commit -m "Initial deployment commit"', "Committing files")
    
    if choice == "1":
        deploy_heroku()
    elif choice == "2":
        deploy_docker()
    elif choice == "3":
        test_local()
    elif choice == "4":
        print("\n📖 Check these files for detailed instructions:")
        print("   - AUTO_DEPLOY.md (Quick start)")
        print("   - DEPLOYMENT.md (Comprehensive guide)")
        print("   - DEPLOYMENT_CHECKLIST.md (Step-by-step)")
    elif choice == "5":
        print("\n👋 Goodbye!")
        sys.exit(0)
    else:
        print("\n❌ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Deployment cancelled")
        sys.exit(0)
