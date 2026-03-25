import urllib.request, urllib.error, urllib.parse, json, time

USERNAME = 'Tanay1202'
TOKEN = '764716e584e92cbe6dce35e2b9521e473f36c715'
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
        return False, f'HTTP {e.code}: {e.read().decode()[:100]}'

def delete_file(path):
    url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{path}'
    req = urllib.request.Request(url, headers=HEADERS, method='DELETE')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code

# Clear consoles first
ok, consoles = api('/consoles/')
if ok and isinstance(consoles, list):
    for c in consoles:
        api(f'/consoles/{c["id"]}/', method='DELETE')
        time.sleep(0.5)
    print(f'Cleared {len(consoles)} consoles')

# Delete the broken venv to free space
print('\nDeleting broken venv (frees ~300MB)...')
ok, result = api('/consoles/', method='POST', data={'executable': 'bash', 'working_directory': f'/home/{USERNAME}'})
cid = result['id']
time.sleep(5)

def send(cmd):
    api(f'/consoles/{cid}/send_input/', method='POST', json_data={'input': cmd + '\n'})

send('rm -rf /home/Tanay1202/.virtualenvs/intrusion-venv && echo DELETED')
print('Sent delete command, waiting 30s...')
time.sleep(30)

# Also delete pip cache
send('rm -rf /home/Tanay1202/.cache/pip && echo CACHE_CLEARED')
time.sleep(15)

# Delete large uploaded files we don't need
large_files = [
    '/home/Tanay1202/Intrusion-Detection01/static/images/istockphoto-1328891609-2048x2048.jpg',
    '/home/Tanay1202/Intrusion-Detection01/static/images/analyser_banner.jpg',
    '/home/Tanay1202/Intrusion-Detection01/static/images/home_first_img.jpg',
    '/home/Tanay1202/Intrusion-Detection01/static/images/login.jpg',
    '/home/Tanay1202/Intrusion-Detection01/static/images/register.jpg',
    '/home/Tanay1202/Intrusion-Detection01/static/images/admin_login.jpeg',
    '/home/Tanay1202/Intrusion-Detection01/static/images/firstimg.jpeg',
    '/home/Tanay1202/Intrusion-Detection01/static/images/hs1.jpg',
    '/home/Tanay1202/Intrusion-Detection01/static/images/hs2.jpg',
    '/home/Tanay1202/Intrusion-Detection01/static/images/hs22.jpg',
    '/home/Tanay1202/setup.sh',
    '/home/Tanay1202/setup.log',
]
print('\nDeleting large/unused files...')
for f in large_files:
    code = delete_file(f)
    print(f'  {f.split("/")[-1]}: {code}')

# Now recreate venv with ONLY what's needed - no pandas/sklearn in venv
# Use system packages instead
print('\nCreating lean venv using system packages...')
send('python3.11 -m venv /home/Tanay1202/.virtualenvs/intrusion-venv --system-site-packages && echo VENV_OK')
time.sleep(20)

send('/home/Tanay1202/.virtualenvs/intrusion-venv/bin/pip install -q --no-cache-dir Flask==2.3.3 gunicorn==21.2.0 && echo FLASK_OK')
print('Installing Flask only (lean install)...')
time.sleep(60)

api(f'/consoles/{cid}/', method='DELETE')

# Reload
DOMAIN = 'Tanay1202.pythonanywhere.com'
ok, r = api(f'/webapps/{DOMAIN}/reload/', method='POST')
print(f'\nReloaded: {ok}')
print(f'Check: https://{DOMAIN}')
