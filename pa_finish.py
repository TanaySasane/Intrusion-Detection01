import urllib.request, urllib.error, urllib.parse, json

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
BASE = 'https://www.pythonanywhere.com/api/v0/user/' + USERNAME
HEADERS = {'Authorization': 'Token ' + TOKEN}
VENV = '/home/Tanay1202/.virtualenvs/intrusion-venv'
PROJECT = '/home/Tanay1202/Intrusion-Detection01'
DOMAIN = 'Tanay1202.pythonanywhere.com'

def api(path, method='GET', json_data=None, data=None):
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

# Set virtualenv + source dir
print('[1] Setting virtualenv and source directory...')
ok, r = api(f'/webapps/{DOMAIN}/', method='PATCH', json_data={
    'virtualenv_path': VENV,
    'source_directory': PROJECT
})
print(f'  {"OK" if ok else r}')

# Reload
print('[2] Reloading web app...')
ok, r = api(f'/webapps/{DOMAIN}/reload/', method='POST')
print(f'  {"Reloaded!" if ok else r}')

# Check web app status
print('[3] Web app status...')
ok, r = api(f'/webapps/{DOMAIN}/')
if ok and isinstance(r, dict):
    print(f'  URL: https://{r.get("domain_name")}')
    print(f'  Status: {r.get("status")}')
    print(f'  Virtualenv: {r.get("virtualenv_path")}')

print(f'\nApp live at: https://{DOMAIN}')
