"""
Upload Flask wheel and install it by extracting directly into site-packages
"""
import urllib.request, urllib.error, zipfile, os, io, time, urllib.parse, json

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
SITE_PACKAGES = '/home/Tanay1202/.virtualenvs/intrusion-venv/lib/python3.11/site-packages'

def upload_bytes(remote_path, content, fname='file'):
    url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{remote_path}'
    boundary = 'PAbound99'
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="content"; filename="{fname}"\r\nContent-Type: application/octet-stream\r\n\r\n'
    ).encode() + content + (f'\r\n--{boundary}--\r\n').encode()
    headers = {'Authorization': 'Token ' + TOKEN, 'Content-Type': f'multipart/form-data; boundary={boundary}'}
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        if e.code in [200, 201]:
            return e.code
        return e.code

# Extract Flask wheel and upload each file
wheel_path = 'flask_wheels/flask-2.3.3-py3-none-any.whl'
print(f'Extracting {wheel_path}...')

with zipfile.ZipFile(wheel_path, 'r') as zf:
    names = zf.namelist()
    flask_files = [n for n in names if n.startswith('flask/') or n.startswith('Flask')]
    print(f'Found {len(flask_files)} Flask files')
    
    for i, name in enumerate(flask_files):
        content = zf.read(name)
        remote = f'{SITE_PACKAGES}/{name}'
        code = upload_bytes(remote, content, name.split('/')[-1])
        if i % 5 == 0:
            print(f'  [{i+1}/{len(flask_files)}] {name} -> {code}')

print('\nFlask files uploaded!')

# Verify
url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{SITE_PACKAGES}/flask/'
req = urllib.request.Request(url, headers={'Authorization': 'Token ' + TOKEN})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(f'Flask dir has {len(data)} files: {list(data.keys())[:5]}')
except urllib.error.HTTPError as e:
    print(f'Flask dir check: {e.code}')

# Reload web app
print('\nReloading web app...')
BASE = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}'
DOMAIN = 'Tanay1202.pythonanywhere.com'
req2 = urllib.request.Request(f'{BASE}/webapps/{DOMAIN}/reload/', headers={'Authorization': 'Token ' + TOKEN}, method='POST')
with urllib.request.urlopen(req2) as resp:
    print('Reloaded:', resp.read().decode())

time.sleep(5)

# Test
print('\nTesting app...')
req3 = urllib.request.Request('https://Tanay1202.pythonanywhere.com', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req3, timeout=15) as resp:
        body = resp.read().decode()
        if 'Hello, World' in body:
            print('Still default - checking error log...')
        else:
            print('SUCCESS! App is live!')
            print(body[:300])
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}')
    print(e.read().decode()[:200])
