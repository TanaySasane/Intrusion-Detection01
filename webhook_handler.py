"""
GitHub Webhook handler - place this at /home/Tanay1202/webhook_handler.py
PA will call this via a separate WSGI endpoint
"""
import subprocess, hmac, hashlib, os, urllib.request, json
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET = 'intrusion-webhook-2026'
PA_TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
PA_USER = 'Tanay1202'
PA_DOMAIN = 'Tanay1202.pythonanywhere.com'
PROJECT = '/home/Tanay1202/Intrusion-Detection01'

@app.route('/github-webhook', methods=['POST'])
def webhook():
    # Verify GitHub signature
    sig = request.headers.get('X-Hub-Signature-256', '')
    body = request.get_data()
    expected = 'sha256=' + hmac.new(SECRET.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return jsonify({'error': 'Invalid signature'}), 403

    # Git pull
    result = subprocess.run(
        ['git', '-C', PROJECT, 'pull', 'origin', 'main'],
        capture_output=True, text=True, timeout=60
    )

    # Reload PA web app
    req = urllib.request.Request(
        f'https://www.pythonanywhere.com/api/v0/user/{PA_USER}/webapps/{PA_DOMAIN}/reload/',
        headers={'Authorization': f'Token {PA_TOKEN}'}, method='POST'
    )
    urllib.request.urlopen(req)

    return jsonify({'status': 'ok', 'output': result.stdout, 'error': result.stderr})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run()
