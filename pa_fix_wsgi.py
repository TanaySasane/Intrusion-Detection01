import urllib.request, urllib.error, json

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
PROJECT = '/home/Tanay1202/Intrusion-Detection01'
VENV = '/home/Tanay1202/.virtualenvs/intrusion-venv'

WSGI_CONTENT = f"""# PythonAnywhere WSGI for Intrusion Detection
import sys, os

path = '{PROJECT}'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['SECRET_KEY'] = 'intrusion-detection-pa-2026'

from app import app as application
"""

def upload(remote_path, content):
    url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{remote_path}'
    boundary = 'PAbound99'
    fname = remote_path.split('/')[-1]
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="content"; filename="{fname}"\r\nContent-Type: text/plain\r\n\r\n'
    ).encode() + content.encode() + f'\r\n--{boundary}--\r\n'.encode()
    headers = {'Authorization': 'Token ' + TOKEN, 'Content-Type': f'multipart/form-data; boundary={boundary}'}
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code

def read_file(remote_path):
    url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{remote_path}'
    headers = {'Authorization': 'Token ' + TOKEN}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode()
    except urllib.error.HTTPError as e:
        return f'ERROR {e.code}'

# Try all possible WSGI paths PA might use
wsgi_paths = [
    f'/var/www/{USERNAME}_pythonanywhere_com_wsgi.py',
    f'/var/www/tanay1202_pythonanywhere_com_wsgi.py',
]

for path in wsgi_paths:
    print(f'Trying: {path}')
    current = read_file(path)
    print(f'  Current content: {current[:100]}')
    code = upload(path, WSGI_CONTENT)
    print(f'  Upload status: {code}')
    # Verify
    updated = read_file(path)
    if 'from app import' in updated:
        print(f'  ✅ WSGI updated successfully at {path}')
    else:
        print(f'  ❌ Update failed')
