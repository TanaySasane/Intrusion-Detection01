import urllib.request, urllib.error, urllib.parse, json, time

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
BASE = 'https://www.pythonanywhere.com/api/v0/user/' + USERNAME
HEADERS = {'Authorization': 'Token ' + TOKEN}
PROJECT_DIR = '/home/Tanay1202/Intrusion-Detection01'
VENV = '/home/Tanay1202/.virtualenvs/intrusion-venv'
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
        return False, f'HTTP {e.code}: {e.read().decode()[:200]}'

# Step 1: Delete old consoles
print('[1] Deleting old consoles...')
ok, consoles = api('/consoles/')
if ok and isinstance(consoles, list):
    for c in consoles:
        cid = c['id']
        ok2, _ = api(f'/consoles/{cid}/', method='DELETE')
        print(f'  Deleted console {cid}: {"ok" if ok2 else "fail"}')
        time.sleep(1)

# Step 2: Create bash console
print('\n[2] Creating bash console...')
ok, result = api('/consoles/', method='POST', data={
    'executable': 'bash',
    'working_directory': '/home/' + USERNAME,
    'arguments': ''
})
if not ok or not isinstance(result, dict):
    print('Failed:', result)
    exit(1)
cid = result['id']
print(f'  Console ID: {cid}')
time.sleep(5)

def send(cmd):
    ok, r = api(f'/consoles/{cid}/send_input/', method='POST', json_data={'input': cmd + '\n'})
    return ok

def get_out():
    ok, r = api(f'/consoles/{cid}/get_latest_output/')
    if ok and isinstance(r, dict):
        return r.get('output', '')
    return ''

# Clear initial output
get_out()
time.sleep(2)

# Step 3: Run setup commands one by one
steps = [
    ('Create venv',       f'python3.11 -m venv {VENV} && echo VENV_OK',                          25),
    ('Upgrade pip',       f'{VENV}/bin/pip install -q --upgrade pip && echo PIP_OK',              20),
    ('Install Flask',     f'{VENV}/bin/pip install -q --prefer-binary Flask Werkzeug gunicorn && echo FLASK_OK', 60),
    ('Install numpy',     f'{VENV}/bin/pip install -q --prefer-binary numpy==1.26.4 && echo NUMPY_OK',           60),
    ('Install pandas',    f'{VENV}/bin/pip install -q --prefer-binary pandas==2.1.4 && echo PANDAS_OK',          90),
    ('Install sklearn',   f'{VENV}/bin/pip install -q --prefer-binary scikit-learn==1.3.2 && echo SKLEARN_OK',   90),
    ('Init DB',           f'{VENV}/bin/python {PROJECT_DIR}/init_db.py && echo DB_OK',            10),
]

for label, cmd, wait in steps:
    print(f'\n  [{label}]')
    send(cmd)
    time.sleep(wait)
    out = get_out()
    lines = [l for l in out.strip().split('\n') if l.strip()]
    last = lines[-1] if lines else '...'
    ok_flag = any(k in out for k in ['_OK', 'DONE', 'success'])
    print(f'  {"✓" if ok_flag else "?"} {last[:120]}')

# Step 4: Set virtualenv + reload
print('\n[4] Configuring web app...')
ok, r = api(f'/webapps/{DOMAIN}/', method='PATCH', json_data={'virtualenv_path': VENV})
print(f'  virtualenv: {"set" if ok else r}')

ok, r = api(f'/webapps/{DOMAIN}/reload/', method='POST')
print(f'  reload: {"done" if ok else r}')

# Cleanup
api(f'/consoles/{cid}/', method='DELETE')

print(f'\n✅ Done! Visit: https://{DOMAIN}')
