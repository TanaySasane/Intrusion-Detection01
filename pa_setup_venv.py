import urllib.request, urllib.error, urllib.parse, json, time

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
PROJECT_DIR = '/home/Tanay1202/Intrusion-Detection01'
VENV = '/home/Tanay1202/.virtualenvs/intrusion-venv'
DOMAIN = 'Tanay1202.pythonanywhere.com'
BASE = 'https://www.pythonanywhere.com/api/v0/user/' + USERNAME
HEADERS = {'Authorization': 'Token ' + TOKEN}

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

# Create a scheduled task to set up venv + install deps + init db
setup_script = (
    f'python3.11 -m venv {VENV} && '
    f'{VENV}/bin/pip install --upgrade pip && '
    f'{VENV}/bin/pip install --prefer-binary Flask==2.3.3 Werkzeug==2.3.7 pandas==2.1.4 scikit-learn==1.3.2 numpy==1.26.4 gunicorn==21.2.0 && '
    f'{VENV}/bin/python {PROJECT_DIR}/init_db.py && '
    f'echo SETUP_COMPLETE'
)

print('[1] Creating setup task...')
ok, result = api('/schedule/', method='POST', json_data={
    'command': setup_script,
    'enabled': True,
    'interval': 'daily',
    'hour': 0,
    'minute': 0,
    'description': 'One-time setup'
})
if ok:
    task_id = result.get('id')
    print(f'  Task created: {task_id}')
else:
    print(f'  {result}')
    task_id = None

# Also try setting virtualenv path now
print('\n[2] Setting virtualenv on web app...')
ok, result = api(f'/webapps/{DOMAIN}/', method='PATCH', json_data={
    'virtualenv_path': VENV
})
print(f'  {"OK" if ok else result}')

# Reload
print('\n[3] Reloading web app...')
ok, result = api(f'/webapps/{DOMAIN}/reload/', method='POST')
print(f'  {"Reloaded!" if ok else result}')

print('\n' + '='*50)
print('Files are uploaded and web app is configured.')
print()
print('FINAL STEP - Open this URL and run ONE command:')
print('https://www.pythonanywhere.com/user/Tanay1202/consoles/new/bash/')
print()
print('Paste this command:')
print()
print(f'python3.11 -m venv {VENV} && {VENV}/bin/pip install --prefer-binary Flask Werkzeug pandas scikit-learn numpy gunicorn && {VENV}/bin/python {PROJECT_DIR}/init_db.py && echo DONE')
print()
print('Then go to Web tab and click Reload.')
print(f'Your app: https://{DOMAIN}')
