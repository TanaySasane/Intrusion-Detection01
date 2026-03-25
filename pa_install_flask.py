import urllib.request, urllib.error, urllib.parse, json, time

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
BASE = 'https://www.pythonanywhere.com/api/v0/user/' + USERNAME
HEADERS = {'Authorization': 'Token ' + TOKEN}
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
        return False, f'HTTP {e.code}: {e.read().decode()[:200]}'

# Clear old consoles
ok, consoles = api('/consoles/')
if ok and isinstance(consoles, list):
    for c in consoles:
        api(f'/consoles/{c["id"]}/', method='DELETE')
        time.sleep(1)
    print(f'Cleared {len(consoles)} consoles')

# New bash console
ok, result = api('/consoles/', method='POST', data={'executable': 'bash', 'working_directory': f'/home/{USERNAME}'})
cid = result['id']
print(f'Console: {cid}')
time.sleep(5)

def send(cmd):
    api(f'/consoles/{cid}/send_input/', method='POST', json_data={'input': cmd + '\n'})

def get_out():
    ok, r = api(f'/consoles/{cid}/get_latest_output/')
    return r.get('output', '') if isinstance(r, dict) else ''

get_out(); time.sleep(2)

# Install flask only (fast)
print('Installing Flask...')
send(f'{VENV}/bin/pip install -q Flask==2.3.3 && echo FLASK_DONE')
for i in range(12):
    time.sleep(10)
    out = get_out()
    if 'FLASK_DONE' in out:
        print('Flask installed!')
        break
    print(f'  [{i+1}] waiting...')

# Reload web app
print('Reloading...')
DOMAIN = 'Tanay1202.pythonanywhere.com'
ok, r = api(f'/webapps/{DOMAIN}/reload/', method='POST')
print('Reloaded:', ok)

api(f'/consoles/{cid}/', method='DELETE')
