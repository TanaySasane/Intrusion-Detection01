import urllib.request, urllib.error, urllib.parse, json, time

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
BASE = 'https://www.pythonanywhere.com/api/v0/user/' + USERNAME
HEADERS = {'Authorization': 'Token ' + TOKEN}
VENV = '/home/Tanay1202/.virtualenvs/intrusion-venv'
PROJECT = '/home/Tanay1202/Intrusion-Detection01'
DOMAIN = 'Tanay1202.pythonanywhere.com'

def api(path, method='GET', data=None, json_data=None):
    url = BASE + path
    headers = dict(HEADERS)
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
        return False, f'HTTP {e.code}: {e.read().decode()[:300]}'

def upload_text(remote_path, content):
    url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{remote_path}'
    boundary = 'PAbound99'
    fname = remote_path.split('/')[-1]
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="content"; filename="{fname}"\r\nContent-Type: text/plain\r\n\r\n').encode() + content.encode() + (f'\r\n--{boundary}--\r\n').encode()
    headers = {'Authorization': 'Token ' + TOKEN, 'Content-Type': f'multipart/form-data; boundary={boundary}'}
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code

# Upload setup script to PA
setup_script = f"""#!/bin/bash
set -e
echo "Creating venv..."
python3.11 -m venv {VENV}
echo "Installing packages..."
{VENV}/bin/pip install -q --prefer-binary Flask==2.3.3 Werkzeug==2.3.7 gunicorn==21.2.0 numpy==1.26.4 pandas==2.1.4 scikit-learn==1.3.2
echo "Init DB..."
{VENV}/bin/python {PROJECT}/init_db.py
echo "SETUP_COMPLETE"
"""

print('[1] Uploading setup script...')
code = upload_text(f'/home/{USERNAME}/setup.sh', setup_script)
print(f'  Uploaded: {code}')

# Delete old consoles
print('\n[2] Clearing consoles...')
ok, consoles = api('/consoles/')
if ok and isinstance(consoles, list):
    for c in consoles:
        api(f'/consoles/{c["id"]}/', method='DELETE')
        time.sleep(1)
    print(f'  Cleared {len(consoles)} consoles')

# Create bash console
print('\n[3] Creating bash console...')
ok, result = api('/consoles/', method='POST', data={'executable': 'bash', 'working_directory': f'/home/{USERNAME}'})
if not ok or not isinstance(result, dict):
    print('Failed:', result)
    exit(1)
cid = result['id']
print(f'  Console: {cid}')
time.sleep(6)

def send(cmd):
    api(f'/consoles/{cid}/send_input/', method='POST', json_data={'input': cmd + '\n'})

def get_out():
    ok, r = api(f'/consoles/{cid}/get_latest_output/')
    return r.get('output', '') if isinstance(r, dict) else ''

# Clear buffer
get_out(); time.sleep(2)

# Run setup script
print('\n[4] Running setup (this takes 4-6 mins)...')
send(f'bash /home/{USERNAME}/setup.sh 2>&1 | tee /home/{USERNAME}/setup.log')

# Poll for completion
for i in range(40):
    time.sleep(15)
    out = get_out()
    if 'SETUP_COMPLETE' in out:
        print('  ✅ Setup complete!')
        break
    if 'error' in out.lower() or 'Error' in out:
        lines = [l for l in out.split('\n') if 'rror' in l]
        print(f'  ⚠ [{i+1}/40] Error detected: {lines[-1][:100] if lines else ""}')
    else:
        lines = [l for l in out.strip().split('\n') if l.strip()]
        last = lines[-1][:100] if lines else '...'
        print(f'  [{i+1}/40] {last}')
else:
    print('  Timed out - check /home/Tanay1202/setup.log on PA')

# Set virtualenv
print('\n[5] Setting virtualenv...')
ok, r = api(f'/webapps/{DOMAIN}/', method='PATCH', json_data={'virtualenv_path': VENV})
print(f'  {"OK" if ok else r}')

# Reload
print('\n[6] Reloading...')
ok, r = api(f'/webapps/{DOMAIN}/reload/', method='POST')
print(f'  {"✅ Reloaded!" if ok else r}')

api(f'/consoles/{cid}/', method='DELETE')
print(f'\n🌐 https://{DOMAIN}')
