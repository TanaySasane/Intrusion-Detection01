import urllib.request, urllib.error, urllib.parse, json, time

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
BASE = 'https://www.pythonanywhere.com/api/v0/user/' + USERNAME
HEADERS = {'Authorization': 'Token ' + TOKEN}
PROJECT_DIR = '/home/Tanay1202/Intrusion-Detection01'
VENV = '/home/Tanay1202/.virtualenvs/intrusion-venv'

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
        return False, f'HTTP {e.code}: {e.read().decode()[:400]}'

# List existing consoles first
print('[0] Checking existing consoles...')
ok, result = api('/consoles/')
if ok:
    consoles = result if isinstance(result, list) else []
    print(f'  Found {len(consoles)} consoles')
    for c in consoles:
        print(f'  - ID:{c["id"]} name:{c["name"]} exe:{c["executable"]}')
else:
    print(' ', result)
    consoles = []

# Reuse existing bash console or create new one
console_id = None
for c in consoles:
    if 'bash' in c.get('executable','').lower() or 'Bash' in c.get('name',''):
        console_id = c['id']
        print(f'  Reusing console {console_id}')
        break

if not console_id:
    print('\n[1] Creating bash console...')
    ok, result = api('/consoles/', method='POST', data={
        'executable': 'bash',
        'working_directory': '/home/' + USERNAME,
        'arguments': ''
    })
    if ok and isinstance(result, dict):
        console_id = result['id']
        print(f'  Created console: {console_id}')
        time.sleep(5)
    else:
        print(f'  Failed: {result}')
        exit(1)

def send(cmd):
    ok, r = api(f'/consoles/{console_id}/send_input/', method='POST', json_data={'input': cmd + '\n'})
    return ok

def get_out():
    ok, r = api(f'/consoles/{console_id}/get_latest_output/')
    if ok and isinstance(r, dict):
        return r.get('output', '')
    return str(r)

# Clear any pending output
get_out()
time.sleep(2)

commands = [
    ('Creating virtualenv', f'python3.11 -m venv {VENV}', 30),
    ('Upgrading pip', f'{VENV}/bin/pip install --upgrade pip -q', 20),
    ('Installing Flask+Werkzeug', f'{VENV}/bin/pip install --prefer-binary -q Flask==2.3.3 Werkzeug==2.3.7 gunicorn==21.2.0', 60),
    ('Installing numpy', f'{VENV}/bin/pip install --prefer-binary -q numpy==1.26.4', 60),
    ('Installing pandas', f'{VENV}/bin/pip install --prefer-binary -q pandas==2.1.4', 90),
    ('Installing scikit-learn', f'{VENV}/bin/pip install --prefer-binary -q scikit-learn==1.3.2', 90),
    ('Init database', f'{VENV}/bin/python {PROJECT_DIR}/init_db.py', 10),
    ('Done check', 'echo ALL_DONE', 5),
]

for label, cmd, wait in commands:
    print(f'\n  >> {label}...')
    send(cmd)
    time.sleep(wait)
    out = get_out()
    last = out.strip().split('\n')[-1] if out.strip() else ''
    print(f'     {last[:100]}')

print('\n[3] Setting virtualenv on web app...')
DOMAIN = 'Tanay1202.pythonanywhere.com'
ok, result = api(f'/webapps/{DOMAIN}/', method='PATCH', json_data={'virtualenv_path': VENV})
print(f'  {"OK" if ok else result}')

print('\n[4] Reloading web app...')
ok, result = api(f'/webapps/{DOMAIN}/reload/', method='POST')
print(f'  {"Reloaded!" if ok else result}')

print('\nDone! Visit: https://' + DOMAIN)
