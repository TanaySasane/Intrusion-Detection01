"""
Full PythonAnywhere deployment via API
- Uploads all project files
- Creates virtualenv
- Installs dependencies
- Creates web app
- Sets WSGI config
"""
import urllib.request, urllib.error, urllib.parse
import json, os, time, mimetypes

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
BASE_URL = 'https://www.pythonanywhere.com/api/v0/user/' + USERNAME
PROJECT_DIR = '/home/' + USERNAME + '/Intrusion-Detection01'
VENV_DIR = '/home/' + USERNAME + '/.virtualenvs/intrusion-venv'
DOMAIN = USERNAME + '.pythonanywhere.com'

def api_request(path, method='GET', data=None, json_data=None):
    url = BASE_URL + path
    headers = {'Authorization': 'Token ' + TOKEN}
    body = None
    if json_data is not None:
        headers['Content-Type'] = 'application/json'
        body = json.dumps(json_data).encode()
    elif data is not None:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            txt = resp.read().decode()
            try: return True, json.loads(txt)
            except: return True, txt
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        return False, f'HTTP {e.code}: {err[:300]}'

def upload_file(remote_path, content_bytes, filename='file'):
    url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{remote_path}'
    boundary = 'PAboundary123456789'
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="content"; filename="{filename}"\r\n'
        f'Content-Type: application/octet-stream\r\n\r\n'
    ).encode() + content_bytes + f'\r\n--{boundary}--\r\n'.encode()
    headers = {
        'Authorization': 'Token ' + TOKEN,
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        if e.code in [200, 201]:
            return e.code, 'ok'
        return e.code, e.read().decode()[:100]

def upload_local_file(local_path, remote_path):
    with open(local_path, 'rb') as f:
        content = f.read()
    code, msg = upload_file(remote_path, content, os.path.basename(local_path))
    return code in [200, 201]

# ── STEP 1: Upload all project files ──────────────────────────────────────────
print('\n[1/5] Uploading project files...')

# Files to upload (local -> remote)
upload_map = {
    'app.py': f'{PROJECT_DIR}/app.py',
    'Database.py': f'{PROJECT_DIR}/Database.py',
    'init_db.py': f'{PROJECT_DIR}/init_db.py',
    'requirements.txt': f'{PROJECT_DIR}/requirements.txt',
    'models/rf_classifier.pkl': f'{PROJECT_DIR}/models/rf_classifier.pkl',
    'models/dt_classifier.pkl': f'{PROJECT_DIR}/models/dt_classifier.pkl',
    'database/db.db': f'{PROJECT_DIR}/database/db.db',
}

# Templates
for tmpl in os.listdir('templates'):
    upload_map[f'templates/{tmpl}'] = f'{PROJECT_DIR}/templates/{tmpl}'

# Static CSS
for css in os.listdir('static/css'):
    upload_map[f'static/css/{css}'] = f'{PROJECT_DIR}/static/css/{css}'

for local, remote in upload_map.items():
    if os.path.exists(local):
        ok = upload_local_file(local, remote)
        status = '✓' if ok else '✗'
        print(f'  {status} {local}')
    else:
        print(f'  - {local} (not found, skipping)')

# Upload static images (skip large ones)
print('  Uploading static images...')
for img in os.listdir('static/images'):
    local = f'static/images/{img}'
    # skip files with spaces, PDFs, and files > 2MB
    if ' ' in img or img.endswith('.pdf'):
        continue
    if os.path.getsize(local) < 2_000_000:
        upload_local_file(local, f'{PROJECT_DIR}/static/images/{img}')
print('  ✓ images done')

# ── STEP 2: Create WSGI file ───────────────────────────────────────────────────
print('\n[2/5] Creating WSGI configuration...')
wsgi_content = f'''
import sys
import os

path = '{PROJECT_DIR}'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['SECRET_KEY'] = 'intrusion-detection-pa-2026'

from app import app as application
'''.encode()

code, msg = upload_file(f'/var/www/{USERNAME}_pythonanywhere_com_wsgi.py', wsgi_content, 'wsgi.py')
print(f'  WSGI file: {code}')

# ── STEP 3: Create web app ─────────────────────────────────────────────────────
print('\n[3/5] Creating web app...')
ok, result = api_request('/webapps/', method='POST', data={
    'domain_name': DOMAIN,
    'python_version': 'python311'
})
if ok:
    print(f'  ✓ Web app created: {DOMAIN}')
else:
    if '409' in str(result) or 'already' in str(result).lower():
        print(f'  Web app already exists, continuing...')
    else:
        print(f'  Result: {result}')

# ── STEP 4: Configure virtualenv ──────────────────────────────────────────────
print('\n[4/5] Setting virtualenv path...')
ok, result = api_request(f'/webapps/{DOMAIN}/', method='PATCH', json_data={
    'virtualenv_path': VENV_DIR,
    'source_directory': PROJECT_DIR,
    'working_directory': PROJECT_DIR,
})
print(f'  ✓ Config updated' if ok else f'  {result}')

# ── STEP 5: Reload web app ────────────────────────────────────────────────────
print('\n[5/5] Reloading web app...')
ok, result = api_request(f'/webapps/{DOMAIN}/reload/', method='POST')
print(f'  ✓ Reloaded' if ok else f'  {result}')

print('\n' + '='*50)
print('DEPLOYMENT COMPLETE!')
print(f'URL: https://{DOMAIN}')
print('='*50)
print()
print('NOTE: You still need to install dependencies.')
print('Go to: https://www.pythonanywhere.com/user/Tanay1202/consoles/')
print('Open a Bash console and run:')
print(f'  mkvirtualenv --python=python3.11 intrusion-venv')
print(f'  pip install -r {PROJECT_DIR}/requirements.txt')
print(f'  python {PROJECT_DIR}/init_db.py')
print(f'  Then reload the web app from the Web tab.')
